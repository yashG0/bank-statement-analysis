import streamlit as st
from pandas import DataFrame
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile
import plotly.express as px
from utils.statement import BankStatementManagement
from utils.config_logger import logger


class StreamlitUiManagement:

    @classmethod
    def page_config(cls) -> None:
        st.set_page_config(
            page_title="Bank Statement Analysis",
            page_icon="💰",
            layout="wide",
            initial_sidebar_state="expanded"
        )

    @classmethod
    def page_setup(cls) -> None:
        st.markdown(
            "<h1 style='text-align: center; color: #4B8BBE;'>📊 Bank Statement Analysis</h1>",
            unsafe_allow_html=True
        )
        st.markdown("### Easily upload, view, and analyze your bank statements with clarity.")

    @classmethod
    def for_upload_file(cls) -> UploadedFile | None:
        file = st.file_uploader("Upload File", type=["csv", "xlsx"])
        if file:
            logger.success("✅ File uploaded successfully!")
            st.success("✅ File uploaded successfully!")
            return file
        return None

    @classmethod
    def for_view_file(cls, uploaded_file: UploadedFile) -> None:
        df: DataFrame | None = BankStatementManagement.to_pandas(uploaded_file)

        if df is None:
            logger.error("❌ Unsupported file type. Please upload a CSV or Excel file.")
            st.error("❌ Unsupported file type. Please upload a CSV or Excel file.")
            return

        tabs = st.tabs(["📁 File Preview", "📊 Data Visualization", "📈 Data Analysis"])

        with tabs[0]:
            st.subheader("📁 File Preview")
            st.dataframe(df, use_container_width=True)

        with tabs[1]:
            st.subheader("📊 Data Visualization")
            if df is not None:
                # Data cleaning and conversion
                df = BankStatementManagement.data_cleansing(df)

            with st.container(border=True):
                sub_tabs = st.tabs(["Line Chart", "Bar Chart", "Histogram", "Pie Chart"])

                # Line Chart
                with sub_tabs[0]:
                    st.markdown("**Trends of Deposits, Withdrawals, and Balance over time**")
                    fig = px.line(df, x='Date', y=['Deposits', 'Withdrawals', 'Balance'],
                                  title="Bank Transactions Over Time")
                    st.plotly_chart(fig)

                # Bar Chart
                with sub_tabs[1]:
                    st.markdown("**Comparison of transaction types by date**")
                    fig = px.bar(df, x='Date', y=['Deposits', 'Withdrawals', 'Balance'],
                                 title="Deposits, Withdrawals, and Balance by Date",
                                 labels={"Date": "Transaction Date", "value": "Amount"})
                    st.plotly_chart(fig)

                # Histogram
                with sub_tabs[2]:
                    st.markdown("**Comparison of transaction types by date**")
                    fig = px.histogram(df, x='Deposits', nbins=20, title="Distribution of Deposits")
                    st.plotly_chart(fig)

                # Pie Chart
                with sub_tabs[3]:
                    st.markdown("**Proportion of total deposits by month or category**")
                    fig = px.pie(df, names='Date', values='Deposits', title="Deposits Distribution")
                    st.plotly_chart(fig)

        with tabs[2]:
            st.subheader("📈 Data Analysis")
            with st.container(border=True):
                if df is not None:
                    # Descriptive Stats
                    st.markdown("### Descriptive Statistics")
                    st.write(df.describe())

                    # Correlation
                    st.markdown("### Correlation Matrix")
                    st.write(BankStatementManagement.get_correlation(df))
                    st.info("Correlation between Deposits, Withdrawals, and Balance.")

                    # Monthly Trend
                    st.markdown("### Monthly Trend")
                    st.line_chart(BankStatementManagement.get_monthly_trends(df))

                    # Outliers
                    st.markdown("### Outliers in Deposits")
                    outliers = BankStatementManagement.detect_outliers(df)
                    st.write(outliers)

                    # Summary
                    st.markdown("### Summary Insights")
                    summary = BankStatementManagement.get_summary(df)
                    st.write(f"Max Deposit: ₹{summary['max_deposit']}")
                    st.write(f"Min Deposit: ₹{summary['min_deposit']}")
                    st.write(f"Max Withdrawal: ₹{summary['max_withdrawal']}")
                    st.write(f"Min Withdrawal: ₹{summary['min_withdrawal']}")
                    st.write(f"Highest deposit occurred on: {summary['max_deposit_date'].strftime('%d-%b-%Y')}")


# --- Main Execution ---
if __name__ == "__main__":
    StreamlitUiManagement.page_config()
    StreamlitUiManagement.page_setup()

    uploaded_file = StreamlitUiManagement.for_upload_file()
    if uploaded_file:
        StreamlitUiManagement.for_view_file(uploaded_file)
