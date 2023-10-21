import requests
from bs4 import BeautifulSoup
import argparse

from data.files import calendar


def fetch_data_for_month(month):
    URL = f"https://www.spin-off.fr/calendrier_des_series.html?date=2023-{month}"
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, "html.parser")

    all_series_data = []

    for cell in soup.select(".floatleftmobile.td_jour"):
        date_div = cell.select_one(".div_jour")
        if date_div:
            date = date_div.select_one("a")["href"].split("date=")[-1]

            for serie in cell.select(".calendrier_episodes"):
                country = serie.find_previous_sibling("img", {"alt": True})["alt"]
                channel_tag = serie.select_one("img[src*='/images/chaines/']")
                channel = channel_tag["alt"] if channel_tag else "N/A"

                all_series_data.append({
                    "channel": channel,
                    "country": country,
                    "date": date
                })
    return all_series_data


def generate_summary(data, month_name):
    total_episodes = len(data)
    countries = {}
    channels = {}
    consecutive_days = {}

    for entry in data:
        country = entry["country"]
        channel = entry["channel"]
        date = entry["date"]

        countries[country] = countries.get(country, 0) + 1
        channels[channel] = channels.get(channel, 0) + 1
        consecutive_days[channel] = consecutive_days.get(channel, [])

        # Logic to compute consecutive days will be a bit more complicated and is omitted for brevity
        # ...

    most_broadcasting_country = max(countries, key=countries.get)
    most_broadcasting_channel = max(channels, key=channels.get)

    print(f"{total_episodes} épisodes seront diffusés pendant le mois de {month_name}.")
    print(
        f"C'est {most_broadcasting_country} qui diffusera le plus d'épisodes avec {countries[most_broadcasting_country]} épisodes.")
    print(
        f"C'est {most_broadcasting_channel} qui diffusera le plus d'épisodes avec {channels[most_broadcasting_channel]} épisodes.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--month", help="Month to generate summary for", required=True)
    args = parser.parse_args()

    month_name = calendar.month_names[args.month]

    data = fetch_data_for_month(args.month)
    generate_summary(data, month_name)
