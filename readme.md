hello
# outlook mail send
import win32com.client as win32

def send_mail():
  outlook = win32.Dispatch('Outlook.Application')
  mail_item = outlook.CreateItem(0) # 0: olMailItem
  mail_item.Recipients.Add('**.**@**.com')
  mail_item.Recipients.Add('**.**@**.com')
  mail_item.Subject = 'Mail Test2'
  mail_item.BodyFormat = 2     # 2: Html format
  mail_item.HTMLBody = '''
Customer PO#	Date/Time Opened	Case Number	Account Name (Local)	Product Code	Serial Number	Cost Type	Internal Summary	Promise Date	Total Price (converted).amount
    '''
  mail_item.Send()
if __name__ == '__main__':
  send_mail()
  

