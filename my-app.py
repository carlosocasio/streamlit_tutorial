import streamlit as st
import numpy as np
import pandas as pd
import pickle  #to load a saved model
import base64  #to open .gif files in streamlit app



# @st.cache_data(suppress_st_warning=True)
@st.cache_data
def get_fvalue(val):    
	feature_dict = {"No":1,"Yes":2}    
	for key,value in feature_dict.items():        
		if val == key:            
			return value
def get_value(val,my_dict):    
	for key,value in my_dict.items():        
		if val == key:            
			return value
app_mode = st.sidebar.selectbox(':blue[Select Page]',['Home','Prediction']) #two pages


css="""
<style>
    [data-testid="stSidebar"] {
        background: LightBlue;
		# color: blue;
    }
</style>
"""
st.write(css, unsafe_allow_html=True)

if app_mode=='Home':   
    st.title('LOAN PREDICTION:')      
    st.image('loan1.jpg')    
    st.markdown('Dataset :')    
    data=pd.read_csv('train.csv')    
    st.write(data.head())    
    st.markdown('Applicant Income VS Loan Amount ')   
    st.bar_chart(data[['ApplicantIncome','LoanAmount']].head(20))

elif app_mode == 'Prediction':     
	st.subheader('Sir/Mme , YOU need to fill all necessary information in order to get a reply to your loan request !')    
	st.sidebar.header(":blue[Information about the client:] ")    
	gender_dict = {":blue[Male]":1,":blue[Female]":2}    
	feature_dict = {":blue[No]":1,":blue[Yes]":2}    
	edu={':blue[Graduate]':1,':blue[Not Graduate]':2}    
	prop={':blue[Rural]':1,':blue[Urban]':2,':blue[Semiurban]':3}    
	ApplicantIncome=st.sidebar.slider(':blue[Applicant Income]',0,10000,0,)    
	CoapplicantIncome=st.sidebar.slider(':blue[Coapplicant Income]',0,10000,0,)    
	LoanAmount=st.sidebar.slider(':blue[Loan Amount in K$]',9.0,700.0,200.0)    
	Loan_Amount_Term=st.sidebar.selectbox(':blue[Loan_Amount_Term]',(12.0,36.0,60.0,84.0,120.0,180.0,40.0,300.0,360.0))    
	Credit_History=st.sidebar.radio(':blue[Credit_History]',(0.0,1.0))    
	Gender=st.sidebar.radio(':blue[Gender]',tuple(gender_dict.keys()))    
	Married=st.sidebar.radio(':blue[Married]',tuple(feature_dict.keys()))    
	Self_Employed=st.sidebar.radio(':blue[Self Employed]',tuple(feature_dict.keys()))    
	Dependents=st.sidebar.radio(':blue[Dependents]',options=[':blue[0]',':blue[1]' , ':blue[2]' , ':blue[3+]'])    
	Education=st.sidebar.radio(':blue[Education]',tuple(edu.keys()))    
	Property_Area=st.sidebar.radio(':blue[Property_Area]',tuple(prop.keys()))    

	class_0,class_1,class_2,class_3 = 0,0,0,0    
	if Dependents == '0':        
		class_0 = 1    
	elif Dependents == '1':        
		class_1 = 1   
	elif Dependents == '2' :        
		class_2 = 1    
	else:        
		class_3= 1    

	Rural,Urban,Semiurban=0,0,0    
	if Property_Area == 'Urban' :        
		Urban = 1    
	elif Property_Area == 'Semiurban' :        
		Semiurban = 1    
	else :        
		Rural=1

	data1={'Gender':Gender,
		'Married':Married,
		'Dependents':[class_0,class_1,class_2,class_3],
		'Education':Education,
		'ApplicantIncome':ApplicantIncome,
		'CoapplicantIncome':CoapplicantIncome,
		'Self Employed':Self_Employed,
		'LoanAmount':LoanAmount,
		'Loan_Amount_Term':Loan_Amount_Term,
		'Credit_History':Credit_History,
		'Property_Area':[Rural,Urban,Semiurban]}    

	feature_list=[ApplicantIncome,
				CoapplicantIncome,
				LoanAmount,
				Loan_Amount_Term,
				Credit_History,
				get_value(Gender,gender_dict),
				get_fvalue(Married),
				data1['Dependents'][0],
				data1['Dependents'][1],
				data1['Dependents'][2],
				data1['Dependents'][3],
				get_value(Education,edu),
				get_fvalue(Self_Employed),
				data1['Property_Area'][0],
				data1['Property_Area'][1],
				data1['Property_Area'][2]]
		
	single_sample = np.array(feature_list).reshape(1,-1)

	if st.button("Predict"):        
		file_ = open("6m-rain.gif", "rb")        
		contents = file_.read()        
		data_url = base64.b64encode(contents).decode("utf-8")        
		file_.close()        

		file = open("green-cola-no.gif", "rb")        
		contents = file.read()        
		data_url_no = base64.b64encode(contents).decode("utf-8")
		file.close()     

		loaded_model = pickle.load(open('RF.sav', 'rb'))        
		prediction = loaded_model.predict(single_sample)        
		if prediction[0] == 0 :            
			st.error('According to our Calculations, you will not get the loan from Bank')
			st.markdown(f'<img src="data:image/gif;base64,{data_url_no}" alt="cat gif">', unsafe_allow_html=True,)
		elif prediction[0] == 1 :
			st.success('Congratulations!! you will get the loan from Bank')
			st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">', unsafe_allow_html=True,)

