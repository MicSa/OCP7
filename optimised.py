import csv

def read_data(file_path):
    """
    This function reads the data from the csv file.
    :param file_path: The path to the csv file.
    :return: A list of tuples representing the shares.
    Each tuple contains the name of the share, its cost and its profit.
    """
    with open(file_path, 'r') as file:
        data = list(csv.reader(file))
    shares = []
    for row in data[1:]:
        shares.append((row[0], int(row[1]), float(row[2].strip('%')) / 100))
    return shares

def knapsack(shares, max_cost):
    """
    This function implements the Knapsack algorithm to find the best combination of shares.
    :param shares: A list of tuples representing the shares.
    :param max_cost: The maximum cost that can be spent on shares.
    :return: The best combination of shares and the maximum profit.
    """
    num_shares = len(shares)
    # Initializing the dynamic programming table.
    dp = [[0] * (max_cost + 1) for _ in range(num_shares + 1)]

    # Filling the dynamic programming table.
    for i in range(1, num_shares + 1):
        share_name, share_cost, share_profit = shares[i - 1]
        for j in range(max_cost + 1):
            if j < share_cost:
                dp[i][j] = dp[i - 1][j]
            else:
                # Choosing the maximum profit between not buying the current share and buying it.
                dp[i][j] = max(dp[i - 1][j], dp[i - 1][j - share_cost] + share_cost * share_profit)

    # The maximum profit is in the bottom-right corner of the table.
    best_profit = dp[-1][-1]
    best_combination = []

    # Tracing back the best combination of shares.
    i, j = num_shares, max_cost
    while i > 0 and j > 0:
        share_name, share_cost, share_profit = shares[i - 1]
        if dp[i][j] != dp[i - 1][j]:
            best_combination.append((share_name, share_cost, share_profit))
            j -= share_cost
        i -= 1

    return best_combination, best_profit

def main():
    """
    This is the main function. It reads the data, calls the Knapsack function and prints the results.
    """
    shares = read_data("Actions1.csv")
    max_cost = 500
    best_combination, best_profit = knapsack(shares, max_cost)
    
    print(f"Best combination: {best_combination}")
    print(f"Best profit: {best_profit:.2f} euros")

if __name__ == "__main__":
    main()
