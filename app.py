from flask import Flask,render_template,request

from src.utills.utils import company_info,load_data,generate_page_content,parse_business_info

app = Flask(__name__)


class DataIngestion:
    def __init__(self):
            self.file_path="./Data/company_data.json"

    def data_loaded(self):
        try:
            company_data=load_data(self.file_path)
            return company_data
        except Exception as e:
            raise ValueError(e)
        
@app.route('/')
def index():
    return render_template('index.html')
   
# Home i have used gpt model to generate content
@app.route('/home',methods=['GET'])
def home():
    try:
        # load_data

        data_obj=DataIngestion()
        company_data=data_obj.data_loaded()

        # split data into separate
        data,business_data=company_info(company_data)

        # Generate Content with OpenAI (GPT-3.5-turbo-instruct Example)
        generate=generate_page_content(data[0],business_data)
        content=[generate]
        customerAction=""
        if data[0]['customerAction']=="":
            customerAction="Get In Touch"
        customerAction=data[0]['customerAction']
        
    
        return render_template('Home.html',content_list=content,cta=customerAction,business_data=business_data)
    except Exception as e:
        raise ValueError(e)

# Used langchain to developed
@app.route('/about',methods=['GET'])
def about():
    try:
        data_obj = DataIngestion()
        company_data = data_obj.data_loaded()

        data, business_data = company_info(company_data)
        data = data[1]  # Assuming the data you need is at index 1 
        data['company_name'] = business_data['businessName']
        customerAction=""

        if data['customerAction']!="":
            customerAction=data['customerAction']

        customerAction="Connect Now"
        generate_data=generate_page_content(data, business_data)
        content=[generate_data]
        print(type(content))
        return render_template('About.html', content_list=content, business_data=business_data,cta=customerAction)
    
    except FileNotFoundError as e:
        raise FileNotFoundError(e)


@app.route('/publications')
def services():
    try:
        data_obj = DataIngestion()
        company_data = data_obj.data_loaded()

        data, business_data = company_info(company_data)
        data = data[2]  # Assuming the data you need is at index 2
        generate_data=generate_page_content(data, business_data)
        
        generate_data['title'] =business_data['businessName']
        keyword=data['seo_keywords'][0]
        
        generate_data['subtitle'] = keyword.split(":")[1]
        # content=[generate_data]
    except Exception as e:
        raise ValueError(e)
    return render_template('Publications.html',content_list=generate_data,business_data=business_data)

@app.route('/contact')
def contact():

    try:
        data_obj = DataIngestion()

        company_data = data_obj.data_loaded()
        data, business_data = company_info(company_data)

        contact_business=parse_business_info(business_data['business_info'])

        return render_template('Contact.html',business_data=business_data,contact_business=contact_business)
    except Exception as e:
        raise ValueError(e)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081,debug=True)