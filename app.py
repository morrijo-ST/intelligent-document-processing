
import html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

def shell(name, title, subtitle, style):
    global PALETTE, INK, PANEL, BG, ACCENT
    themes = {
      'terminal': ('#091411','#10221d','#e7f5ee','#3fe0a0','#7e9c8d',4),
      'purple': ('#171625','#222137','#f5f1ff','#ba9bff','#9ca1c0',12),
      'indigo': ('#f4f5fb','#ffffff','#242746','#5149b9','#64708b',18),
      'coral': ('#faf7f2','#ffffff','#302a27','#c7543e','#796d65',20),
      'blue': ('#f2f6fa','#ffffff','#183348','#126bb5','#5d7486',8),
      'cyan': ('#07141d','#102330','#def5ff','#53d2ed','#8caab9',4),
      'ops': ('#0b1720','#132733','#e7f5f4','#4edbc4','#99b5bd',10),
      'editorial': ('#f8f7f3','#ffffff','#253b38','#317764','#6b7d77',6),
      'amber': ('#17212c','#223140','#f8f4e9','#efbc67','#a6b2bf',6),
    }
    BG,PANEL,INK,ACCENT,MUTED,RADIUS=themes[style]
    PALETTE=[ACCENT,'#4c9fd6','#d99455','#ae83c6','#6cae8b']
    px.defaults.color_discrete_sequence=PALETTE
    st.markdown(f"""<style>
    .stApp {{background:{BG};color:{INK}}}
    [data-testid="stHeader"] {{background:{BG};}}
    .block-container {{max-width:1480px;padding:2rem 2.5rem 4rem;}}
    [data-testid="stSidebar"] {{background:{PANEL};border-right:1px solid {MUTED}35;}}
    h1,h2,h3,p,label,[data-testid="stMarkdownContainer"], [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{color:{INK};}}
    h1 {{font-size:2.55rem!important;letter-spacing:-.055em;line-height:1.12!important;font-weight:650!important;}}
    h2,h3 {{letter-spacing:-.025em;}}
    [data-testid="stCaptionContainer"] p {{color:{MUTED}!important;}}
    [data-testid="stMetric"] {{background:{PANEL};border:1px solid {MUTED}30;border-top:2px solid {ACCENT};border-radius:{RADIUS}px;padding:18px 20px;}}
    [data-testid="stMetricValue"] {{font-variant-numeric:tabular-nums;font-size:1.8rem;}}
    [data-testid="stPlotlyChart"] {{background:{PANEL};border:1px solid {MUTED}30;border-radius:{RADIUS}px;overflow:hidden;}}
    [data-baseweb="select"] > div, [data-baseweb="input"], [data-baseweb="base-input"], textarea {{background:{PANEL}!important;color:{INK}!important;}}
    input,textarea {{color:{INK}!important;-webkit-text-fill-color:{INK}!important;}}
    [data-baseweb="tag"] {{background:{ACCENT}25!important;color:{INK}!important;}}
    [data-baseweb="tag"] span {{color:{INK}!important;}}
    button[kind="secondary"], [data-testid="stDownloadButton"] button {{background:{PANEL};color:{INK};border-color:{MUTED}65;}}
    [data-baseweb="tab"] {{color:{INK}!important;}}
    [data-testid="stAlert"] {{background:{PANEL};color:{INK};}}
    .eyebrow {{font:600 11px ui-monospace,monospace;letter-spacing:.15em;color:{ACCENT};margin-bottom:16px;}}
    .hero {{border-bottom:1px solid {MUTED}40;padding:12px 0 25px;margin-bottom:24px;}}
    .hero p {{max-width:850px;color:{MUTED};font-size:1rem;}}
    .brief {{border-left:3px solid {ACCENT};background:{PANEL};padding:16px 20px;margin:18px 0;color:{INK};}}
    @media(max-width:700px){{.block-container{{padding:1rem;}}h1{{font-size:1.8rem!important;}}}}
    </style>""",unsafe_allow_html=True)
    st.markdown(f'<div class="hero"><div class="eyebrow">MORRIS / {html.escape(name.upper())} · SYNTHETIC DEMO</div><h1>{html.escape(title)}</h1><p>{html.escape(subtitle)}</p></div>',unsafe_allow_html=True)
    st.sidebar.caption('MORRIS · PORTFOLIO LAB')
    st.sidebar.caption('Fictional data. Explore the workflow; no external systems are connected.')

def chart(fig, height=340):
    fig.update_layout(template='plotly_white',paper_bgcolor=PANEL,plot_bgcolor=PANEL,font=dict(color=INK,size=12),colorway=PALETTE,height=height,margin=dict(l=55,r=25,t=55,b=55),legend=dict(orientation='h',y=-.24,x=0),hoverlabel=dict(bgcolor=PANEL,font_color=INK))
    fig.update_xaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    fig.update_yaxes(automargin=True,gridcolor='rgba(128,145,155,.14)',zerolinecolor='rgba(128,145,155,.3)')
    st.plotly_chart(fig,use_container_width=True,theme=None)

def brief(text):
    st.markdown('<div class="brief">'+html.escape(text)+'</div>',unsafe_allow_html=True)

def money(value):
    sign='−' if value<0 else ''
    return f'{sign}${abs(value)/1e6:,.2f}M' if abs(value)>=1e6 else f'{sign}${abs(value):,.0f}'

def metrics(items):
    for col,(label,value) in zip(st.columns(len(items)),items):col.metric(label,value)

def table(df, name='detail', height=360):
    config={}
    for col in df.columns:
        label=str(col).replace('_',' ').title()
        if pd.api.types.is_numeric_dtype(df[col]) and not pd.api.types.is_bool_dtype(df[col]):
            if any(x in str(col) for x in ['pct','margin','confidence','attainment','probability','achievement']):
                config[col]=st.column_config.NumberColumn(label,format='%.3f')
            elif any(x in str(col) for x in ['amount','revenue','arr','acv','cost','expense','cash','earned','capitalized','amortization','balance','asset','budget','forecast','variance','value','backlog','receipts','payroll','subcontractor','materials','labor']):
                config[col]=st.column_config.NumberColumn(label,format='$%.2f')
            else:config[col]=st.column_config.NumberColumn(label)
        else:config[col]=st.column_config.Column(label)
    st.dataframe(df,use_container_width=True,hide_index=True,height=height,column_config=config)
    st.download_button('Download '+name.replace('_',' ')+' CSV',df.to_csv(index=False),name+'.csv','text/csv',key='export_'+name)

def nonempty(df):
    if df.empty:
        st.info('No records in this selection. Choose at least one filter value to continue.')
        st.stop()

import random
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Intelligent Document Processing",layout="wide")
shell('DOCUMENT REVIEW','Evidence first. Approval second.','Compare invoice fields against purchase orders and review duplicate, variance, and confidence controls.','blue')
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
f['match_status']=f.apply(lambda r:'Duplicate' if r.duplicate else ('Matched' if abs(r.variance)<=max(25,r.po_amount*.02) and r.confidence>=threshold else 'Review'),axis=1)


metrics([('Documents',str(len(f))),('Matched',str(int(f.match_status.eq('Matched').sum()))),('Review',str(int(f.match_status.eq('Review').sum()))),('Duplicate candidates',str(int(f.match_status.eq('Duplicate').sum())))])
brief('Synthetic extracted fields, not live OCR. Duplicate controls take precedence over the confidence threshold. Changing the threshold re-evaluates all non-duplicate documents.')
a,b=st.columns([1.35,1])
with a:
    st.subheader('Exception inbox')
    exc=f[f.match_status!='Matched'].sort_values(['duplicate','confidence'],ascending=[False,True])
    table(exc,'document_exceptions')
with b:
    st.subheader('Document evidence')
    selected=st.selectbox('Document',f.document_id.tolist())
    r=f[f.document_id==selected].iloc[0]
    st.write(f'**{r.invoice_number}** / {r.vendor}')
    st.caption('Synthetic field card · no source PDF attached')
    st.write(f'Invoice: **{money(r.invoice_amount)}**')
    st.write(f'{r.po_number}: **{money(r.po_amount)}**')
    st.write(f'Difference: **{money(r.variance)}**')
    tolerance=max(25,r.po_amount*.02)
    checks=pd.DataFrame({'Control':['Duplicate reference','Amount tolerance','Confidence threshold'],'Result':['Blocked' if r.duplicate else 'Pass','Pass' if abs(r.variance)<=tolerance else 'Review','Pass' if r.confidence>=threshold else 'Review']})
    st.dataframe(checks,hide_index=True,use_container_width=True)
    st.caption(f'Amount tolerance: {money(tolerance)}. Simulated extraction score: {r.confidence:.0%}.')
with st.expander('Processing analysis'):
    chart(px.scatter(f,x='po_amount',y='invoice_amount',color='match_status',hover_name='invoice_number',color_discrete_map={'Duplicate':'#ba4545','Review':'#be8d29','Matched':'#278578'},title='Invoice against purchase order'))
    table(f,'document_register')
