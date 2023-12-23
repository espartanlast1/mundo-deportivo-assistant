import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
import itertools
import time
import os
from concurrent.futures import ProcessPoolExecutor, as_completed
import warnings
from collections import Counter
import numpy as np

warnings.filterwarnings("ignore")


def evaluate_arima_model(data, arima_order):
    try:
        model = ARIMA(data, order=arima_order)
        model_fit = model.fit()
        error = mean_squared_error(data, model_fit.fittedvalues)
        return (arima_order, error)
    except Exception as e:
        print(f"Error in model evaluation for order {arima_order}: {e}")
        return (arima_order, float("inf"))


def plot_arima_predictions(data, order, player_name, forecast_days):
    try:
        model = ARIMA(data, order=order)
        model_fit = model.fit()

        # In-sample prediction
        in_sample_pred = model_fit.predict(start=data.index[0], end=data.index[-1])

        # Out-of-sample forecast
        forecast = model_fit.get_forecast(steps=forecast_days)
        forecast_index = pd.date_range(start=data.index[-1], periods=forecast_days + 1, freq=data.index.freq)[1:]
        forecast_values = forecast.predicted_mean

        # Plot actual data, in-sample predictions, and out-of-sample forecast
        plt.figure(figsize=(12, 6))
        plt.plot(data, label='Actual Data', color='blue')
        plt.plot(in_sample_pred, label='In-sample Prediction', alpha=0.7, color='green')
        plt.plot(forecast_index, forecast_values, label=f'{forecast_days}-day Forecast', alpha=0.7, color='orange')
        plt.title(f'ARIMA Model Validation and {forecast_days}-day Forecast for {player_name}')
        plt.xlabel('Date')
        plt.ylabel('Value')
        plt.legend()
        plt.savefig(f'{player_name}_arima_plot.png')
        plt.close()
        print(f"Plot saved for {player_name}")
    except Exception as e:
        print(f"Error in plotting for {player_name}: {e}")



def arima_grid_search(data, p_values, d_values, q_values, player_name):
    best_score, best_order = float("inf"), None
    for order in itertools.product(p_values, d_values, q_values):
        _, error = evaluate_arima_model(data, order)
        if error < best_score:
            best_score, best_order = error, order
        print(f"Processing {player_name}, ARIMA order: {order}, Current Best: {best_order}", end='\r')
    plot_arima_predictions(data, best_order, player_name, 60)
    return best_order


def process_batch(batch_id, players, df, p_values, d_values, q_values):
    results = {}
    print(f"\nStarting batch {batch_id} processing with {len(players)} players.")
    for player in players:
        print(f"\nStarting ARIMA grid search for {player}...")
        player_data = df[df['Name'] == player]['Value']
        if len(player_data) < 30:
            print(f"Skipping {player} due to insufficient data.")
            continue
        best_order = arima_grid_search(player_data, p_values, d_values, q_values, player)
        results[player] = best_order
        print(f"\nCompleted ARIMA grid search for {player}. Best order: {best_order}")
    print(f"Completed processing batch {batch_id}.")
    return results


def main():
    df = pd.read_csv('fantasy-market-variation.csv')
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True)
    df.set_index('Date', inplace=True)

    p_values = range(0, 3)
    d_values = range(0, 2)
    q_values = range(0, 3)
    num_cores = os.cpu_count() - 2

    players = df['Name'].unique()
    batch_size = int(np.ceil(len(players) / num_cores))
    player_batches = [players[i:i + batch_size] for i in range(0, len(players), batch_size)]

    all_params = []
    player_best_params = {}

    print(f"Number of cores available: {num_cores}")
    print("Starting parallel ARIMA grid search across batches...")
    start_time = time.time()
    try:
        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            futures = {executor.submit(process_batch, i, batch, df, p_values, d_values, q_values): i for i, batch in
                       enumerate(player_batches)}

            for future in as_completed(futures):
                batch_id = futures[future]
                batch_results = future.result()
                player_best_params.update(batch_results)
                all_params.extend(batch_results.values())
                print(
                    f"\nCompleted processing for batch {batch_id}. Total progress: {len(player_best_params)}/{len(players)} players.")
    except Exception as e:
        print(f"Error in parallel processing: {e}")
        print("Reverting to sequential processing...")
        for i, batch in enumerate(player_batches):
            results = process_batch(i, batch, df, p_values, d_values, q_values)
            player_best_params.update(results)
            all_params.extend(results.values())

    elapsed_time = time.time() - start_time
    print(f"\nCompleted ARIMA grid search for all players in {elapsed_time:.2f} seconds.")

    for player, params in player_best_params.items():
        print(f"{player}: {params}")

    most_common_params = Counter(all_params).most_common(1)[0][0]
    print("\nMost Common ARIMA Parameters (Generic Model) for All Players:")
    print(f"P: {most_common_params[0]}, D: {most_common_params[1]}, Q: {most_common_params[2]}")


if __name__ == '__main__':
    main()