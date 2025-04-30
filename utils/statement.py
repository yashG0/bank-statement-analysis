from pandas import DataFrame
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile
from utils.config_logger import logger


class BankStatementManagement:

    @staticmethod
    def to_pandas(uploaded_file: UploadedFile) -> DataFrame | None:
        try:
            logger.info(f"Received file: {uploaded_file.name}")
            if uploaded_file.name.endswith('.csv'):
                logger.info("Reading CSV file")
                return pd.read_csv(uploaded_file)

            elif uploaded_file.name.endswith('.xlsx'):
                logger.info("Reading Excel file")
                return pd.read_excel(uploaded_file)

            else:
                logger.warning(f"Unsupported file format: {uploaded_file.name}")
                return None

        except Exception as e:
            logger.exception(f"Failed to read file {uploaded_file.name}: {e}")
            return None

    @staticmethod
    def size_of_data(df: DataFrame) -> int:
        size = df.size
        logger.info(f"Data size: {size}")
        return size

    @staticmethod
    def data_cleansing(df: DataFrame) -> DataFrame:
        try:
            logger.info("Starting data cleansing")
            df['Deposits'] = pd.to_numeric(df['Deposits'].str.replace(',', '').fillna(0))
            df['Withdrawals'] = pd.to_numeric(df['Withdrawals'].str.replace(',', '').fillna(0))
            df['Balance'] = pd.to_numeric(df['Balance'].str.replace(',', '').fillna(0))
            df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%Y')
            logger.info("Data cleansing completed")
            return df
        except Exception as e:
            logger.exception(f"Error during data cleansing: {e}")
            return df

    @staticmethod
    def get_summary(df: DataFrame) -> dict:
        try:
            logger.info("Calculating summary statistics")
            summary = {
                "max_deposit": df["Deposits"].max(),
                "min_deposit": df["Deposits"].min(),
                "max_withdrawal": df["Withdrawals"].max(),
                "min_withdrawal": df["Withdrawals"].min(),
                "max_deposit_date": df.loc[df["Deposits"].idxmax(), "Date"]
            }
            logger.info(f"Summary: {summary}")
            return summary
        except Exception as e:
            logger.exception(f"Error calculating summary: {e}")
            return {}

    @staticmethod
    def get_correlation(df: DataFrame) -> DataFrame:
        try:
            logger.info("Computing correlation matrix")
            return df[['Deposits', 'Withdrawals', 'Balance']].corr()
        except Exception as e:
            logger.exception(f"Error computing correlation: {e}")
            return pd.DataFrame()

    @staticmethod
    def get_monthly_trends(df: DataFrame) -> DataFrame:
        try:
            logger.info("Generating monthly trend data")
            return df[['Date', 'Deposits', 'Withdrawals']].set_index('Date').resample('M').sum()
        except Exception as e:
            logger.exception(f"Error generating monthly trends: {e}")
            return pd.DataFrame()

    @staticmethod
    def detect_outliers(df: DataFrame) -> DataFrame:
        try:
            logger.info("Detecting outliers in Deposits")
            Q1 = df['Deposits'].quantile(0.25)
            Q3 = df['Deposits'].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df['Deposits'] < (Q1 - 1.5 * IQR)) | (df['Deposits'] > (Q3 + 1.5 * IQR))][
                ['Date', 'Deposits']]
            logger.info(f"Outliers found: {len(outliers)}")
            return outliers
        except Exception as e:
            logger.exception(f"Error detecting outliers: {e}")
            return pd.DataFrame()
