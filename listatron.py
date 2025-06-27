import streamlit as st
import pandas as pd
import io
from datetime import datetime, date, timedelta

def process_dataframe(df):
    try:
        # Fix the column mapping. CSV columns are shifted
        df_corrected = pd.DataFrame({
            'Gender': df['Load#'].str.strip(),        # Actual gender is in Load# column
            'Division': df['Gender'].str.strip(),     # Division is in Gender column  
            'Style': df['Division'].str.strip(),      # Style is in Division column
            'Color': df['Style'].str.strip(),         # Color is in Style column
            'Size': df['Color'].str.strip(),          # Size is in Color column
            'Qty': df[' "EU Size"']                   # Quantity is in "EU Size" column
        })
       
        # Clean up
        df_corrected['Gender'] = df_corrected['Gender'].str.strip()
        df_corrected['Style'] = df_corrected['Style'].astype(str).str.strip()
        df_corrected['Color'] = df_corrected['Color'].str.strip()
       
        # Check and make sure Qty is numeric
        df_corrected['Qty'] = pd.to_numeric(df_corrected['Qty'], errors='coerce') #If Qty value is not a number, turn to NaN
        df_corrected = df_corrected.dropna(subset=['Qty']) #Drop all NaN and only keep numbers
       
        # Group and sum
        # Groups data with same Gender, Style, Color and sums the Qty of each group
        grouped_df = df_corrected.groupby(['Gender', 'Style', 'Color'])['Qty'].sum().reset_index()
        # Changes Qty for Total and shows the total of each group 
        grouped_df.columns = ['Gender', 'Style', 'Color', 'Total']
       
        # Filter into categories
        men_df = grouped_df[grouped_df['Gender'] == 'MENS']
        women_df = grouped_df[grouped_df['Gender'] == 'WOMENS']
        kids_df = grouped_df[grouped_df['Gender'].isin(['BOYS', 'GIRLS']) & ~grouped_df['Style'].str.endswith('N')]
        work_df = grouped_df[grouped_df['Gender'] == 'INDUSTRIAL']
        nano_df = grouped_df[grouped_df['Style'].str.endswith('N')]
        
        # Calculate total quantity from original corrected dataframe
        total_qty = df_corrected['Qty'].sum()
        
        return men_df, women_df, kids_df, work_df, nano_df, total_qty, None
        
    except Exception as e:
        return None, None, None, None, None, 0, str(e)

def create_excel_file(men_df, women_df, kids_df, work_df, nano_df):
    # Create Excel file in memory and return as bytes bc idk
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        men_df.to_excel(writer, sheet_name='Men', index=False)
        women_df.to_excel(writer, sheet_name='Women', index=False)
        kids_df.to_excel(writer, sheet_name='Kids', index=False)
        nano_df.to_excel(writer, sheet_name='Nano', index=False)
        work_df.to_excel(writer, sheet_name='Work', index=False)
    
    return output.getvalue()

# Streamlit App
st.title('🚀 LISTATRON 505')

# Sidebar - Day Counter Utility
st.sidebar.title("🗓️ Contador de días")

# Start date input
start_date = st.sidebar.date_input("Fecha de compra")

# Calculate date 45 days from start_date
date_plus_45 = start_date + timedelta(days=45)

# End date input (optional)
use_today = st.sidebar.checkbox("Hasta HOY", value=True)

if use_today:
    end_date = date.today()
else:
    end_date = st.sidebar.date_input("Elegir fecha", min_value=start_date)

# Calculate difference and display
if start_date and end_date:
    delta = end_date - start_date
    
    # Show action dependent on time
    if delta.days > 45:
        st.sidebar.subheader(f"**{start_date.strftime('%d %b %Y')}** - **{end_date.strftime('%d %b %Y')}**")
        st.sidebar.title(f"📅 **{delta.days}** días")
        st.sidebar.markdown("---")
        st.sidebar.title(":red[❌ _No se puede hacer el cambio_]")
    elif delta.days == 1:
        st.sidebar.subheader(f"**{start_date.strftime('%d %b %Y')}** - **{end_date.strftime('%d %b %Y')}**")
        st.sidebar.title(f"📅 **{delta.days}** día")
        st.sidebar.markdown("---")
        st.sidebar.title(":green[✅ _Se puede hacer el cambio_]")
    elif delta.days > 1 and delta.days <= 45:
        st.sidebar.subheader(f"**{start_date.strftime('%d %b %Y')}** - **{end_date.strftime('%d %b %Y')}**")
        st.sidebar.title(f"📅 **{delta.days}** días")
        st.sidebar.markdown("---")
        st.sidebar.title(":green[✅ _Se puede hacer el cambio_]")
    elif delta.days < 0:
        st.sidebar.title(":red[Error!❌ Esa fecha es en el futuro]")
        st.sidebar.subheader(f"Faltan {abs(delta.days)} dias para llegar")
    elif delta.days == 0:
        st.sidebar.markdown("---")
        st.sidebar.title(f"Es hoy!")
        st.sidebar.markdown(f"📅 **45 días después**: {date_plus_45.strftime('%d/%m/%Y')}")


st.write('Carga el archivo y se descarga ordenado papá')

# File uploader
uploaded_file = st.file_uploader("Elegí el archivo", type="csv")

if uploaded_file is not None:
    try:
        # Read the CSV file
        df = pd.read_csv(uploaded_file)
        
        # Process the data
        men_df, women_df, kids_df, work_df, nano_df, total_qty, error = process_dataframe(df)
        
        if error:
            st.error(f"Error: {error}")
        else:
            st.success(f"Se subio tuani! Total pares: {int(total_qty)}")

            # Create and offer download
            excel_data = create_excel_file(men_df, women_df, kids_df, work_df, nano_df)
            
            st.markdown("---")
            st.subheader("📥 Descargame dog")
            st.download_button(
                label="📥 Descargar archivo ordenado",
                data=excel_data,
                file_name="data_sorted.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.success("Se guardó tuani! Descargalo dog")
            st.markdown("---")

            st.subheader("Preview para revisar que todo Gucci")
            
            # Show summary with total Qty for each category
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                men_total = men_df['Total'].sum() if not men_df.empty else 0
                st.metric("Men", f"{int(men_total)}", f"{len(men_df)} refes")
            with col2:
                women_total = women_df['Total'].sum() if not women_df.empty else 0
                st.metric("Women", f"{int(women_total)}", f"{len(women_df)} refes")
            with col3:
                kids_total = kids_df['Total'].sum() if not kids_df.empty else 0
                st.metric("Kids", f"{int(kids_total)}", f"{len(kids_df)} refes")
            with col4:
                work_total = work_df['Total'].sum() if not work_df.empty else 0
                st.metric("Work", f"{int(work_total)}", f"{len(work_df)} refes")
            with col5:
                nano_total = nano_df['Total'].sum() if not nano_df.empty else 0
                st.metric("Nano", f"{int(nano_total)}", f"{len(nano_df)} refes")
            
            # Show preview of each category
            categories = {
                "Men": men_df,
                "Women": women_df,
                "Kids": kids_df,
                "Work": work_df,
                "Nano": nano_df
            }
            
            for category, data in categories.items():
                if not data.empty:
                    with st.expander(f"Preview {category} data"):
                        st.dataframe(data)
            

    except Exception as e:
        st.error(f"Error leyendo: {str(e)}")
else:
    st.info("Tiene que ser CSV")

st.markdown("---")
st.markdown("*SM type shit*")