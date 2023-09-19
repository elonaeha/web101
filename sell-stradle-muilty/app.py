
import cred as c
from flask import Flask ,render_template ,request ,redirect,url_for

def otplogin(otp):
    from NorenRestApiPy.NorenApi import  NorenApi


    class ShoonyaApiPy(NorenApi):
        def __init__(self):
            NorenApi.__init__(self, host='https://api.shoonya.com/NorenWClientTP/', websocket='wss://api.shoonya.com/NorenWSTP/')        
            global api
            api = self

    import logging
    
    logging.basicConfig(level=logging.DEBUG)

    api = ShoonyaApiPy()

    opt = otp
    ret = api.login(userid=c.user, password=c.pwd, twoFA=opt, vendor_code=c.vc, api_secret=c.app_key, imei=c.imei)
    return ret['uname']

def sorder(index ,strike1,strike2, expry,cepetype,qty,ortype):
    if strike2:
            exch  = 'NFO'
            if cepetype == "STD":
                queryc = f'{index} {strike2} {expry} CE' 
                queryp = f'{index} {strike2} {expry} PE' 
                ret = api.searchscrip(exchange=exch, searchtext=queryc)

                if ret != None:
                    symbols = ret['values']
                    symble = symbols[0]['tsym']
                    c.s2ce = symble
                ret = api.searchscrip(exchange=exch, searchtext=queryp)

                if ret != None:
                    symbols = ret['values']
                    symble = symbols[0]['tsym']
                    c.s2pe = symble
            
            else:
                query = f'{index} {strike2} {expry} {cepetype}' 
                ret = api.searchscrip(exchange=exch, searchtext=query)

                if ret != None:
                    symbols = ret['values']
                    symble = symbols[0]['tsym']
                    

                ret = api.place_order(buy_or_sell=ortype, product_type='I',
                                                    exchange='NFO', tradingsymbol=symble, 
                                                    quantity=qty, discloseqty=0,price_type='MKT', price=0,
                                                    retention='DAY', remarks='my_order_001')
            exch  = 'NFO'
            if cepetype == "STD":
                queryc = f'{index} {strike1} {expry} CE' 
                queryp = f'{index} {strike1} {expry} PE' 
                ret = api.searchscrip(exchange=exch, searchtext=queryc)

                if ret != None:
                    symbols = ret['values']
                    symble = symbols[0]['tsym']
                    c.s1ce = symble
                ret = api.searchscrip(exchange=exch, searchtext=queryp)

                if ret != None:
                    symbols = ret['values']
                    symble = symbols[0]['tsym']
                    c.s1pe = symble
                    

                ret = api.place_order(buy_or_sell=ortype, product_type='I',
                                                    exchange='NFO', tradingsymbol=c.s1pe, 
                                                    quantity=qty, discloseqty=0,price_type='MKT', price=0,
                                                    retention='DAY', remarks='my_order_001')
                ret = api.place_order(buy_or_sell=ortype, product_type='I',
                                                    exchange='NFO', tradingsymbol=c.s1ce, 
                                                    quantity=qty, discloseqty=0,price_type='MKT', price=0,
                                                    retention='DAY', remarks='my_order_001')
                ret = api.place_order(buy_or_sell=ortype, product_type='I',
                                                    exchange='NFO', tradingsymbol=c.s2pe, 
                                                    quantity=qty, discloseqty=0,price_type='MKT', price=0,
                                                    retention='DAY', remarks='my_order_001')
                ret = api.place_order(buy_or_sell=ortype, product_type='I',
                                                    exchange='NFO', tradingsymbol=c.s2ce, 
                                                    quantity=qty, discloseqty=0,price_type='MKT', price=0,
                                                    retention='DAY', remarks='my_order_001')
            
            else:
                query = f'{index} {strike1} {expry} {cepetype}' 
                ret = api.searchscrip(exchange=exch, searchtext=query)

                if ret != None:
                    symbols = ret['values']
                    symble = symbols[0]['tsym']
                    

                ret = api.place_order(buy_or_sell=ortype, product_type='I',
                                                    exchange='NFO', tradingsymbol=symble, 
                                                    quantity=qty, discloseqty=0,price_type='MKT', price=0,
                                                    retention='DAY', remarks='my_order_001')
    else:
            exch  = 'NFO'
            if cepetype == "STD":
                queryc = f'{index} {strike1} {expry} CE' 
                queryp = f'{index} {strike1} {expry} PE' 
                ret = api.searchscrip(exchange=exch, searchtext=queryc)

                if ret != None:
                    symbols = ret['values']
                    symble = symbols[0]['tsym']
                    c.ce = symble
                ret = api.searchscrip(exchange=exch, searchtext=queryp)

                if ret != None:
                    symbols = ret['values']
                    symble = symbols[0]['tsym']
                    c.pe = symble
                    

                ret = api.place_order(buy_or_sell=ortype, product_type='I',
                                                    exchange='NFO', tradingsymbol=c.pe, 
                                                    quantity=qty, discloseqty=0,price_type='MKT', price=0,
                                                    retention='DAY', remarks='my_order_001')
                ret = api.place_order(buy_or_sell=ortype, product_type='I',
                                                    exchange='NFO', tradingsymbol=c.ce, 
                                                    quantity=qty, discloseqty=0,price_type='MKT', price=0,
                                                    retention='DAY', remarks='my_order_001')
            
            else:
                query = f'{index} {strike1} {expry} {cepetype}' 
                ret = api.searchscrip(exchange=exch, searchtext=query)

                if ret != None:
                    symbols = ret['values']
                    symble = symbols[0]['tsym']
                    

                ret = api.place_order(buy_or_sell=ortype, product_type='I',
                                                    exchange='NFO', tradingsymbol=symble, 
                                                    quantity=qty, discloseqty=0,price_type='MKT', price=0,
                                                    retention='DAY', remarks='my_order_001')
            
            

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/home', methods=['POST'])
def verify_otp():
    user_otp = request.form['otp']
    login = otplogin(user_otp)
    c.disuser = login
    return render_template('home.html',name = login)



@app.route('/form', methods=['GET', 'POST'])
def form():
    message = ""
    if request.method == 'POST':
        # Access form data using request.form.get()
        index = request.form.get('optionType')
        strike1 = request.form.get('strike1')
        strike2 = request.form.get('strike2')
        expiry = request.form.get('expiry')
        qty = request.form.get('qty')
        option_type = request.form.get('optiontype')
        order_type = request.form.get('ordertype')

        # Call the order function with form data
        sorder(index, strike1,strike2 ,expiry, option_type,qty,order_type)
        message = "Form submitted successfully!"

        # Return a response or redirect
        
    return render_template('home.html', message=message,name = c.disuser)

    # Render the form on GET request
    


if __name__ == '__main__':
    app.run(debug=True)
