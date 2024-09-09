import csv
import matplotlib.pyplot as plt

def load_sales_data(csv_file):
    """Loads sales data from the given CSV file."""
    sales_data = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            sales_data.append({
                'Item': row['Item'],
                'Quantity': int(row['Quantity']),
                'Total': float(row['Total'])
            })
    return sales_data

def plot_sales_data(sales_data):
    """Plots sales data using a bar chart."""
    items = [data['Item'] for data in sales_data]
    quantities = [data['Quantity'] for data in sales_data]
    totals = [data['Total'] for data in sales_data]

    # Create a bar chart
    plt.figure(figsize=(10, 6))

    # Bar chart for quantities
    plt.subplot(1, 2, 1)
    plt.bar(items, quantities, color='blue')
    plt.xlabel('Items')
    plt.ylabel('Quantity Sold')
    plt.title('Quantity of Each Item Sold')
    plt.xticks(rotation=60, ha='right')

    # Bar chart for total prices
    plt.subplot(1, 2, 2)
    plt.bar(items, totals, color='green')
    plt.xlabel('Items')
    plt.ylabel('Total Revenue ($)')
    plt.title('Revenue per Item')
    plt.xticks(rotation=60, ha='right')

    # Adjust layout to avoid clipping the labels
    plt.tight_layout()

    # Save the plot to a file (save before showing)
    plt.savefig('sales_summary.png')
    print("[INFO] Sales summary saved as 'sales_summary.png'")

    # Show the plot
    plt.show()

if __name__ == "__main__":
    # Load the sales data from CSV
    sales_data = load_sales_data('sales_data.csv')

    # Plot the sales data
    plot_sales_data(sales_data)
