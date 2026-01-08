# Amazon Sales Data Pipeline

An end-to-end data engineering pipeline for processing and analyzing Amazon sales data using Apache Spark, Kafka, Airflow, and Streamlit.

## 📋 Project Overview

This project implements a scalable data pipeline that:
- Ingests Amazon sales data from CSV files
- Processes data in batch using Apache Spark
- Streams real-time data using Apache Kafka
- Orchestrates workflows with Apache Airflow
- Visualizes insights through interactive Streamlit dashboards
- Stores processed data in Parquet format for efficient querying

## 🏗️ Architecture

```
├── airflow/          # Workflow orchestration
│   └── dags/         # Airflow DAG definitions
├── dashboard/        # Data visualization
│   └── streamlit_app.py
├── data/
│   ├── raw/          # Raw CSV data
│   │   ├── amazon.csv
│   │   └── download.py
│   └── parquet/      # Processed data in Parquet format
├── kafka/            # Real-time streaming
│   └── producer.py
├── spark/            # Batch processing
│   └── batch_processing.py
└── docker-compose.yml
```

## 🛠️ Tech Stack

- **Batch Processing**: Apache Spark (PySpark)
- **Stream Processing**: Apache Kafka
- **Workflow Orchestration**: Apache Airflow
- **Visualization**: Streamlit
- **Storage**: Parquet
- **Containerization**: Docker, Docker Compose
- **Language**: Python 3.x

## 📊 Features

### Batch Processing (Spark)
- **Data Cleaning**: Filters null values, validates price and rating data
- **Sales Analysis by Category**: 
  - Total products per category
  - Average discounted price
  - Average rating
  - Total rating count
- **Top-Rated Products**: Identifies highly-rated products (>4.5 rating, >35K reviews)
- **Efficient Storage**: Saves processed data in Parquet format with optional partitioning

### Real-time Streaming (Kafka)
- Kafka producer for real-time data ingestion
- Enables event-driven data processing

### Orchestration (Airflow)
- Automated workflow scheduling
- DAG-based pipeline management

### Dashboard (Streamlit)
- Interactive data visualization
- Real-time metrics and insights

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Python 3.x
- Minimum 8GB RAM recommended

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd amazon-sales-pipeline
```

2. **Start the services using Docker Compose**
```bash
docker-compose up -d
```

3. **Download the data** (if not already present)
```bash
python data/raw/download.py
```

### Running the Pipeline

#### Batch Processing
```bash
# Run Spark batch processing
python spark/batch_processing.py
```

#### Kafka Producer
```bash
# Start Kafka producer
python kafka/producer.py
```

#### Streamlit Dashboard
```bash
# Launch the dashboard
streamlit run dashboard/streamlit_app.py
```

## 📈 Data Schema

The pipeline processes Amazon product data with the following schema:

| Field | Type | Description |
|-------|------|-------------|
| product_id | String | Unique product identifier |
| Product_name | String | Product name |
| category | String | Product category |
| discounted_price | Float | Current selling price |
| actual_Price | Float | Original price |
| discount_percentage | Float | Discount percentage |
| rating | Float | Product rating (0-5) |
| rating_count | Integer | Number of ratings |

## 📁 Output

Processed data is saved in the `data/parquet/` directory:
- `sales_by_category/` - Aggregated sales metrics by category
- `top_rated_products/` - Top-rated products analysis

## 🔧 Configuration

- **Spark Configuration**: Modify `batch_processing.py` for Spark settings
- **Kafka Configuration**: Update `producer.py` for Kafka broker settings
- **Airflow DAGs**: Add/modify DAGs in `airflow/dags/` directory
- **Docker Services**: Configure services in `docker-compose.yml`

## 📝 Usage Examples

### Analyzing Sales by Category
The pipeline automatically groups products by category and calculates:
- Total number of products
- Average discounted price
- Average rating
- Total rating count

### Finding Top-Rated Products
Identifies products with:
- Rating > 4.5
- Rating count > 35,000
- Sorted by popularity (rating count)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

[Your Name]

## 🙏 Acknowledgments

- Amazon product dataset
- Apache Spark community
- Apache Kafka community
- Streamlit team
