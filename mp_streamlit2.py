import streamlit as st
import pandas as pd
import io

def process_dataframe(df):
    """Process the uploaded dataframe and return categorized dataframes"""
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
       
        # Clean up and ensure proper data types
        df_corrected['Gender'] = df_corrected['Gender'].str.strip()
        df_corrected['Style'] = df_corrected['Style'].astype(str).str.strip()
        df_corrected['Color'] = df_corrected['Color'].str.strip()
       
        # Ensure Qty is numeric
        df_corrected['Qty'] = pd.to_numeric(df_corrected['Qty'], errors='coerce')
        df_corrected = df_corrected.dropna(subset=['Qty'])
       
        # Group and sum
        grouped_df = df_corrected.groupby(['Gender', 'Style', 'Color'])['Qty'].sum().reset_index()
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
    """Create Excel file in memory and return as bytes"""
    output = io.BytesIO()
    
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        men_df.to_excel(writer, sheet_name='Men', index=False)
        women_df.to_excel(writer, sheet_name='Women', index=False)
        kids_df.to_excel(writer, sheet_name='Kids', index=False)
        work_df.to_excel(writer, sheet_name='Work', index=False)
        nano_df.to_excel(writer, sheet_name='Nano', index=False)
    
    return output.getvalue()

# Streamlit App
st.title('🚀 LISTATRON 505')
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
            
            # Show a preview of the original data
            #   with st.expander("Un preview de la data para asegurar que todo Gucci"):
            #       st.dataframe(df.head())

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

# Footer
st.markdown("---")
st.markdown("*SM type shit*")