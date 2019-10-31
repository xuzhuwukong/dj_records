from django.shortcuts import render, HttpResponse, redirect
from app01 import models
from app01 import forms
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import json


# Create your views here.


# =================维修时间：==================
# 管理维修时间
@login_required()
def periods(request):
    authors_obj = models.Period.objects.all()
    return render(request, 'periods.html', {"user_login": auth.get_user(request), "authors_obj": authors_obj, })


# 增加维修时间
@login_required()
def period_add(request):
    if request.method == "POST":
        author_status = forms.CheckAuthor(request.POST)
        if author_status.is_valid():
            author_name = request.POST.get("author_name")
            models.Period.objects.create(
                name=author_name,
            )
            print("已新增维修时间", author_name)
            return redirect("/periods/")
        else:
            pass
    return render(request, 'period_add.html', {"user_login": auth.get_user(request)})


# 删除维修时间
@login_required()
def period_delete(request, author_id):
    author_obj = models.Period.objects.filter(nid=author_id).first()
    print("已删除维修时间", author_obj.name)
    author_obj.delete()
    return redirect("/periods/")


# 编辑维修时间信息
@login_required()
def period_edit(request, author_id):
    author_obj = models.Period.objects.filter(nid=author_id).first()
    if request.method == "POST":
        author_status = forms.CheckAuthor(request.POST)
        if author_status.is_valid():
            author_name = request.POST.get("author_name")
            models.Period.objects.filter(nid=author_id).update(
                name=author_name,
            )
            print("已更新维修时间", author_name)
            return redirect("/periods/")
        else:
            pass
    return render(request, 'period_add.html', {"user_login": auth.get_user(request), "author_obj": author_obj})


# =================工程师：==================
# 管理工程师
@login_required()
def engineers(request):
    publish_obj = models.Engineer.objects.all()
    return render(request, 'engineers.html', {"user_login": auth.get_user(request), "publish_obj": publish_obj, })


# 增加工程师
@login_required()
def engineer_add(request):
    if request.method == "POST":
        publish_status = forms.CheckPublish(request.POST)
        if publish_status.is_valid():
            publish_name = request.POST.get("publish_name")
            publish_email = request.POST.get("publish_email")
            publish_addr = request.POST.get("publish_addr")
            models.Engineer.objects.create(name=publish_name, email=publish_email, addr=publish_addr)
            print("已新增出版社", publish_name)
            return redirect("/engineers/")
        else:
            pass
    return render(request, 'engineer_add.html', {"user_login": auth.get_user(request)})


# 删除工程师
@login_required()
def engineer_delete(request, publish_id):
    publish_obj = models.Engineer.objects.filter(nid=publish_id).first()
    print("已删除工程师", publish_obj.name)
    publish_obj.delete()
    return redirect("/engineers/")


# 编辑工程师信息
@login_required()
def engineer_edit(request, publish_id):
    publish_obj = models.Engineer.objects.filter(nid=publish_id).first()
    if request.method == "POST":
        publish_status = forms.CheckPublish(request.POST)
        if publish_status.is_valid():
            publish_name = request.POST.get("publish_name")
            publish_email = request.POST.get("publish_email")
            publish_addr = request.POST.get("publish_addr")
            models.Engineer.objects.filter(nid=publish_id).update(name=publish_name, email=publish_email,
                                                                 addr=publish_addr)
            print("已更新工程师", publish_name)
            return redirect("/engineers/")
        else:
            pass
    return render(request, 'engineer_add.html', {"user_login": auth.get_user(request), "publish_obj": publish_obj})


# =================订单：==================
# 管理订单
@login_required()
def records(request):
    records_obj = models.Record.objects.all()
    return render(request, 'records.html', {"records_obj": records_obj, "user_login": auth.get_user(request)})


# 增加订单
@login_required()
def record_add(request):
    publish_obj = models.Engineer.objects.all()
    author_obj = models.Period.objects.all()
    if request.method == "POST":
        book_status = forms.CheckBook(request.POST)
        if book_status.is_valid():
            book_name = request.POST.get("book_name")
            # 检查订单是否已存在：
            book_name_check = models.Record.objects.filter(title=book_name)
            if book_name_check:
                response_msg = "《" + book_name + "》" + "订单已存在，请重新输入！"
                print(response_msg)
                return HttpResponse(response_msg)

            book_price = request.POST.get("book_price")
            book_pub_date = request.POST.get("book_pub_date")
            book_pub_id = request.POST.get("book_pub_id")
            book_author_id_list = request.POST.getlist("book_author_id_list")
            book_obj = models.Record.objects.create(
                title=book_name,
                price=book_price,
                publish_date=book_pub_date,
                engineer_id=book_pub_id,
            )
            book_obj.periods.add(*book_author_id_list)
            print("已新增订单", book_name)
            return redirect("/records/")
        else:
            pass
    return render(request, 'record_add.html', {
        "user_login": auth.get_user(request),
        "publish_obj": publish_obj,
        "author_obj": author_obj,
    })


# 删除订单
@login_required()
def record_delete(request, book_id):
    book_obj = models.Record.objects.filter(nid=book_id).first()
    print("已删除订单", book_obj.title)
    book_obj.delete()
    return redirect("/records/")


# 编辑订单信息
@login_required()
def record_edit(request, book_id):

    publish_obj = models.Engineer.objects.all()
    author_obj = models.Period.objects.all()
    publish_obj_dict = publish_obj.values_list("pk", "name")
    author_obj_dict = author_obj.values("pk", "name")
    new_publish_obj_dict = []
    new_author_obj_dict = []
    for item in publish_obj_dict:
        new_publish_obj_dict.append(item)
    for item in author_obj_dict:
        new_author_obj_dict.append(item)

    if request.method == "POST":
        book_obj = models.Record.objects.filter(pk=book_id).first()
        print(book_obj,book_id)
        post_flag = request.POST.get("post_flag")
        if post_flag == "edit_btn":
            # 获取当前选择的订单信息，加载到模态框中：
            book_name = book_obj.title
            book_price = book_obj.price
            book_pub_date = book_obj.publish_date
            book_pub_id = book_obj.publish.pk
            new_book_author_id_list = []
            book_author_id_list = book_obj.authors.all().values_list("pk")
            for i in book_author_id_list:
                new_book_author_id_list.append(i[0])
            # print(new_book_author_id_list)

            # 点击编辑按钮以后，在此生成json数据，返回当前订单的信息给客户端ajax，然后渲染模态框：
            json_data = {
                "book_name": book_name,
                "book_price": str(book_price),
                "book_pub_date": str(book_pub_date),
                "book_pub_id": book_pub_id,
                "new_book_author_id_list": new_book_author_id_list,
                "new_publish_obj_dict": new_publish_obj_dict,
                "new_author_obj_dict": new_author_obj_dict,
            }
            json_data = json.dumps(json_data)
            return HttpResponse(json_data)
        else:
            # 解析修改订单信息以后提交的表单数据，并更新数据库：
            book_status = forms.CheckBook(request.POST)
            if book_status.is_valid():
                book_name = request.POST.get("post_book_name")
                # 检查订单是否已存在：
                book_name_check = models.Record.objects.filter(title=book_name)
                if book_name_check:
                    response_msg = "《" + book_name + "》" + "订单已存在，请重新输入！"
                    print(response_msg)
                    return HttpResponse(response_msg)

                book_price = request.POST.get("post_book_price")
                book_pub_date = request.POST.get("post_book_pub_date")
                book_pub_id = request.POST.get("post_book_pub_id")
                book_author_id_list = request.POST.get("post_book_author_id_list")
                # 将字符串格式的列表转换为真正的列表：
                book_author_id_list = json.loads(book_author_id_list)

                models.Record.objects.filter(nid=book_id).update(
                    title=book_name,
                    price=book_price,
                    publish_date=book_pub_date,
                    publish_id=book_pub_id,
                )
                book_obj.authors.clear()
                book_obj.authors.add(*book_author_id_list)
                print("已更新订单", book_name)
                return HttpResponse("订单信息修改完毕！")
            else:
                pass

    # 如下代码为不采用ajax方式提交数据，由django的render方法渲染订单修改的页面：
    # publish_obj = models.Publish.objects.all()
    # author_obj = models.Period.objects.all()
    # book_obj = models.Book.objects.filter(nid=book_id).first()
    # if request.method == "POST":
    #     book_status = forms.CheckBook(request.POST)
    #     if book_status.is_valid():
    #         book_name = request.POST.get("book_name")
    #         book_price = request.POST.get("book_price")
    #         book_pub_date = request.POST.get("book_pub_date")
    #         book_pub_id = request.POST.get("book_pub_id")
    #         book_author_id_list = request.POST.getlist("book_author_id_list")
    #         models.Book.objects.filter(nid=book_id).update(
    #             title=book_name,
    #             price=book_price,
    #             publish_date=book_pub_date,
    #             publish_id=book_pub_id,
    #         )
    #         book_obj.authors.clear()
    #         book_obj.authors.add(*book_author_id_list)
    #         print("已更新订单", book_name)
    #         return redirect("/books/")
    #     else:
    #         pass
    # return render(request, 'record_add.html', {
    #     "user_login": auth.get_user(request),
    #     "book_obj": book_obj,
    #     "publish_obj": publish_obj,
    #     "author_obj": author_obj,
    # })


# =================注册、登陆、注销：==================
# 登陆
def login(request):
    error_msg = ""
    if request.method == "POST":
        user_obj = forms.LoginCheck(request.POST)
        if user_obj.is_valid():
            id_username = request.POST.get("id_username")
            id_password = request.POST.get("id_password")
            user_auth_obj = auth.authenticate(username=id_username, password=id_password)
            if user_auth_obj:
                auth.login(request, user_auth_obj)
                print(id_username, "登陆成功！")
                return redirect("/records/")
            else:
                error_msg = "用户名或密码错误！"
        else:
            print(user_obj.errors)
            error_msg = "登陆字段校验不通过！"

    return render(request, 'login.html', {"error_msg": error_msg, "user_login": auth.get_user(request)})


# 注册
def reg(request):
    error_msg = ""
    if request.method == "POST":
        user_obj = forms.RegCheck(request.POST)
        if user_obj.is_valid():
            id_username = request.POST.get("id_username")
            id_password = request.POST.get("id_password")
            id_password2 = request.POST.get("id_password2")
            if User.objects.filter(username=id_username):
                error_msg = "用户名已存在！"
            else:
                if id_password == id_password2:
                    new_user = User.objects.create_user(username=id_username, password=id_password)
                    print(new_user.username, "用户创建成功！")
                    return redirect("/login/")
                else:
                    error_msg = "密码不一致！"
        else:
            error_msg = "字段校验不通过！"

    return render(request, "reg.html", {"error_msg": error_msg})


# 注销
@login_required()
def logout(request):
    print(auth.get_user(request), "注销登陆！")
    auth.logout(request)
    return redirect("/login/")


def orders(request):
    orders_obj = models.Order.objects.all()
    return render(request, 'orders.html', {"orders_obj": orders_obj, "user_login": auth.get_user(request)})



def add_order(request):
    """
    后台管理的添加订单视图函数
    :param request:
    :return:
    """
    order_list_to_insert = []
    if request.method == "POST":
        content = request.POST.get("content")
        content = content.strip("\r\n").split("\r\n")
        if(content[0].split("\t")[0] == "Customer PO#" and content[0].split("\t")[-1]=="Total Price (converted).amount"):
            for c in content[1:]:
                print(c.split("\t"))
                order_list_to_insert.append(models.Order(*c))
            models.Order.objects.bulk_create(order_list_to_insert)
        return redirect("/orders/")
    return render(request, "add_order.html")