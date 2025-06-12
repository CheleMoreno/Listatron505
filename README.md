# Listatron 505

Listatron 505 is a simple, no-nonsense web app that lets you upload messy CSVs, cleans and organizes the data into categories (Men, Women, Kids, Industrial, Nano), and gives you back a beautiful Excel file ready to use. It also includes a quick return policy day counter built right into the sidebar.

## Features

- Upload a CSV file and instantly get:
  - Cleaned and grouped data by `Gender`, `Style`, `Color`, and total quantity.
  - Separate sheets for each category in the output Excel file.
- Integrated day counter:
  - Input a purchase date and check if a return is valid based on a 45-day policy.
- Simple and efficient interface powered by Streamlit.

## How It Works


1. Upload your CSV file.
2. The app maps the scrambled columns to their correct meanings.
3. It cleans the data and converts quantities into numerical values.
4. Then it groups the products and creates an organized Excel file.
5. Download the result instantly and review the categorized summaries.

## Technologies Used

- Python 3
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [XlsxWriter](https://xlsxwriter.readthedocs.io/)

## Usage

1. Clone the repo:

```bash
git clone https://github.com/CheleMoreno/listatron505.git
cd listatron505
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
streamlit run app.py
```

4. Open the web app in your browser and upload your file.

## Screenshots

Home page:


![image](https://github.com/user-attachments/assets/840ccb2d-e081-4eb3-85c1-563a4322b0be)


Loaded doc:


![image](https://github.com/user-attachments/assets/45542d76-9c05-46bd-bf53-1ec87e9582ff)


Counter between dates:


![image](https://github.com/user-attachments/assets/fd9e18f4-99c8-4c97-9764-c4c108506cf5)




