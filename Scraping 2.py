import os
import csv
import requests
from bs4 import BeautifulSoup


try:
    match_date = input("Enter the date in the format MM-DD-YY: ")
    page = requests.get(f"https://www.yallakora.com/match-center/%d9%85%d8%b1%d9%83%d8%b2-%d8%a7%d9%84%d9%85%d8%a8%d8%a7%d8%b1%d9%8a%d8%a7%d8%aa?date={match_date}")
    page.raise_for_status()  # Check if the request was successful
except requests.exceptions.RequestException as e:
    print(f"Error fetching the page: {e}")
    exit()

def main(page):
    src = page.content
    soup = BeautifulSoup(src, 'lxml')
    matches_details = []

    # Find all championship cards
    championships = soup.find_all("div", {"class": "matchCard"})

    def get_match_info(champ):
        try:
            champ_title = champ.contents[1].find("h2").text.strip()
        except AttributeError:
            champ_title = "Unknown Championship"

        # Find all individual matches within this championship
        all_matches = champ.find_all("div", {"class": "item finish liItem"})
        for match in all_matches:
            try:
                # Teams of match
                team_a = match.find("div", {"class": "teams teamA"}).text.strip()
                team_b = match.find("div", {"class": "teams teamB"}).text.strip()

                # Match Time
                match_time = match.find("span", {"class": "time"}).text.strip()

                # Result
                match_result = match.find("div", {"class": "MResult"}).find_all("span", {"class": "score"})
                score = f"{match_result[0].text.strip()}::{match_result[1].text.strip()}"
                score = str(score)
                # Append to details
                matches_details.append({
                    "Championship": champ_title, 
                    "Team A": team_a, 
                    "Team B": team_b, 
                    "Match Time": match_time, 
                    "Score": score
                })
            except AttributeError:
                continue  # Skip if any element is not found

    for champ in championships:
        get_match_info(champ)

    # Ensure the output directory exists
    output_dir = r"C:\Users\PC\scraping"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "football.csv")
    
    try:
        with open(output_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Championship", "Team A", "Team B", "Match Time", "Score"])
            writer.writeheader()
            writer.writerows(matches_details)
        print(f"Data successfully written to {output_path}")
    except Exception as e:
        print(f"Error writing to file: {e}")

main(page)
