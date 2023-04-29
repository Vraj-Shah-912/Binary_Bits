@app.route('/sendmail',method=['POST','GET'])
# def sendmail():
#     if request.method == 'POST':
#         try:
#             formlink = request.form.get('formlink')
#         except:
#             flash("user not found","danger")
#             return redirect('/forgot')
#         flash("reset email has send " ,"success")
#         return redirect('/')
#     else:
#         return 0
