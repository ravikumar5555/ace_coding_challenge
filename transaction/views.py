import traceback

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from .models import Transaction, LineItem, InventoryItem, DepartmentMaster, CompanyLedgerMaster, BranchMaster, \
    ArticleMaster, ColorMaster

from .response_helper import ResponseHelper
from .operation_helper import OperationHelper
ResponseHelper = ResponseHelper()
OperationHelper = OperationHelper()


class TransactionView(APIView):

    def post(self, request):
        """
        POST API to add transaction
        :param request: http request
        :return: response
        """
        data = request.data.copy()
        if not data:
            return ResponseHelper.get_status_404("request does not have any data")
        try:
            ##### create a transaction #####
            company = get_object_or_404(CompanyLedgerMaster, name=data["company"])
            branch = get_object_or_404(BranchMaster, short_name = data["branch"])
            department = get_object_or_404(DepartmentMaster, name=data["department"])
            trans = Transaction(company=company, branch=branch, department=department,
                                transaction_status= data["status"], remarks=data["remarks"])
            trans.save()

            ##### add line items #####
            for litem in data["line_items"]:
                article = get_object_or_404(ArticleMaster, name=litem["article"])
                color = get_object_or_404(ColorMaster, name=litem["color"])
                line_item = LineItem(article=article, color=color, required_on_date= litem["req_date"],
                                     quantity=litem["quantity"], rate_per_unit=litem["rate_per_unit"],
                                     unit=litem["unit"], transaction_id=trans)
                line_item.save()

                ##### add inventory #####
                for inv in litem["inventory_items"]:
                    article = get_object_or_404(ArticleMaster, name=inv["article"])
                    color = get_object_or_404(ColorMaster, name=inv["color"])
                    company = get_object_or_404(CompanyLedgerMaster, name=inv["company"])
                    inv_item = InventoryItem(article=article, color=color, company=company,
                                             gross_quantity=inv["gross_quantity"], net_quantity=inv["net_quantity"],
                                             unit=inv["unit"], line_item_id=line_item)
                    inv_item.save()

        except:
            traceback.print_exc()
            return ResponseHelper.get_status_500("error in saving data")
        output_response = {
            "transaction_id": trans.id,
            "transaction_number": trans.transaction_number
        }
        return ResponseHelper.get_status_201(msg="transaction is sucessful", data=output_response)

    def delete(self, request):
        """
        API to delete transaction
        :param request:
        :return:
        """
        ##### get transaction id from query parameter #####
        trans_id = request.GET.get("transaction_id", "")
        if not trans_id:
            return ResponseHelper.get_status_422("transaction_id is missing or blank in query parameter")

        ##### check if transaction is database #####
        try:
            trans = Transaction.objects.get(id=int(trans_id))
        except Transaction.DoesNotExist:
            return ResponseHelper.get_status_404("transaction not found in database")

        ##### check if any line item with this transaction id #####
        litems = LineItem.objects.filter(transaction_id_id=int(trans_id))
        if not litems:
            #### no line line items in this transaction, so can delete #####
            Transaction.objects.filter(id=int(trans_id)).delete()
        else:
            ##### for each line item check if inventory is created, if its created then cant delete transaction #####
            for item in litems:
                inv_items = InventoryItem.objects.filter(line_item_id_id=item.id)
                if inv_items:
                    #### inventory created, cant delete #####
                    return ResponseHelper.get_status_409("can not delete transaction as inventory deleted")
            else:
                ##### line items added but inventort is not added so can delete transaction #####
                Transaction.objects.filter(id=int(trans_id)).delete()

        return ResponseHelper.get_status_200("transaction deleted successfully")

    def get(self, request):
        """
        GET API to get transation details
        :param request:
        :return:
        """
        ##### get transaction id from query parameter #####
        trans_id = request.GET.get("transaction_id", "")
        if not trans_id:
            return ResponseHelper.get_status_422("transaction_id is missing or blank in query parameter")

        ##### get transaction data #####
        try:
            trans = Transaction.objects.get(id=int(trans_id))
        except Transaction.DoesNotExist:
            return ResponseHelper.get_status_404("transaction not found in database")
        trans_data = OperationHelper.to_dict(trans)

        ##### get company name, dept name, branch name #####
        final_response = trans_data.copy()

        ##### get company data #####
        try:
            company = CompanyLedgerMaster.objects.get(id=trans_data["company"])
        except CompanyLedgerMaster.DoesNotExist:
            return ResponseHelper.get_status_404("company not found in database")
        final_response["company"] = OperationHelper.to_dict(company)["name"]

        ##### get branch data #####
        try:
            branch = BranchMaster.objects.get(id=trans_data["branch"])
        except BranchMaster.DoesNotExist:
            return ResponseHelper.get_status_404("branch not found in database")
        final_response["branch"] = OperationHelper.to_dict(branch)["short_name"]

        ##### get department data #####
        try:
            dept = DepartmentMaster.objects.get(id=trans_data["department"])
        except DepartmentMaster.DoesNotExist:
            return ResponseHelper.get_status_404("department not found in database")
        final_response["department"] = OperationHelper.to_dict(dept)["name"]

        ##### get data for line items #####
        line_items = LineItem.objects.filter(transaction_id_id=int(trans_id))
        if line_items:
            line_item_list = [OperationHelper.to_dict(x) for x in line_items]
            for item in line_item_list:
                invs = InventoryItem.objects.filter(line_item_id_id=item["id"])
                inv_data = [OperationHelper.to_dict(x) for x in invs]
                item["inventory_items"] = inv_data
            final_response["line_items"] = line_item_list

        return ResponseHelper.get_status_200(data=final_response)