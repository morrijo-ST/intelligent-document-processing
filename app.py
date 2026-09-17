import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Intelligent Document Processing",layout="wide")
st.title("Intelligent Document Processing")
st.caption("Synthetic invoice extraction, PO matching, confidence scoring, duplicate controls, and exception routing.")
random.seed(55)
rows=[]
for i in range(160):
    po=f"PO-{random.randint(1001,1085)}"
    invoice=f"INV-{2000+i}"
    po_amount=round(random.uniform(250,24000),2)
    invoice_amount=round(po_amount*random.uniform(.97,1.04),2)
    confidence=round(random.uniform(.72,.99),2)
    vendor=random.choice(["Northstar Supplies","Apex Cloud","Summit Services","Metro Logistics","Vertex Media"])
    rows.append({"document_id":f"DOC-{i+1:04}","invoice_number":invoice,"vendor":vendor,"po_number":po,"po_amount":po_amount,"invoice_amount":invoice_amount,"confidence":confidence})
df=pd.DataFrame(rows)
for idx in [15,41,98]:
    df.loc[idx,"invoice_number"]=df.loc[idx-1,"invoice_number"]
df["variance"]=df.invoice_amount-df.po_amount
df["duplicate"]=df.duplicated("invoice_number",keep=False)
df["match_status"]=df.apply(lambda r:"Duplicate" if r.duplicate else ("Matched" if abs(r.variance)<=max(25,r.po_amount*.02) and r.confidence>=.85 else "Review"),axis=1)

threshold=st.sidebar.slider("Extraction confidence threshold",0.70,0.98,0.85,0.01)
f=df.copy()
f.loc[f.confidence<threshold,"match_status"]="Review"

c1,c2,c3,c4=st.columns(4)
c1.metric("Documents",len(f))
c2.metric("Auto-matched",int((f.match_status=="Matched").sum()))
c3.metric("Review",int((f.match_status=="Review").sum()))
c4.metric("Duplicates",int((f.match_status=="Duplicate").sum()))

st.subheader("Processing outcomes")
out=f.groupby("match_status",as_index=False).size()
st.plotly_chart(px.pie(out,names="match_status",values="size"),use_container_width=True)

left,right=st.columns(2)
with left:
    st.subheader("Invoice vs PO")
    st.plotly_chart(px.scatter(f,x="po_amount",y="invoice_amount",color="match_status",hover_name="invoice_number",hover_data=["vendor","confidence"]),use_container_width=True)
with right:
    st.subheader("Extraction confidence")
    st.plotly_chart(px.histogram(f,x="confidence",color="match_status",nbins=15),use_container_width=True)

st.subheader("Exception queue")
exc=f[f.match_status!="Matched"].sort_values(["duplicate","confidence"],ascending=[False,True])
st.dataframe(exc[["document_id","invoice_number","vendor","po_number","po_amount","invoice_amount","variance","confidence","match_status"]],use_container_width=True,hide_index=True)
st.info("Production implementations would add OCR/vision extraction, document storage, ERP API calls, approval workflows, and immutable audit logs. This demo focuses on the control logic after extraction.")
