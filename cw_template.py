"""
****************************************************************************
Additional info
 1. I declare that my work contins no examples of misconduct, such as
 plagiarism, or collusion.
 2. Any code taken from other sources is referenced within my code solution.
 3. Student ID: w2121958
 4. Date: 20/11/2025
****************************************************************************

"""
from graphics import *
import csv
import os

data_list = []   # data_list An empty list to load and hold data from csv file

VALID_AIRPORTS = {
    "LHR": "London Heathrow",
    "MAD": "Madrid Adolfo Suárez-Barajas",
    "CDG": "Charles De Gaulle International",
    "IST": "Istanbul Airport International",
    "AMS": "Amsterdam Schiphol",
    "LIS": "Lisbon Portela",
    "FRA": "Frankfurt Main",
    "FCO": "Rome Fiumicino",
    "MUC": "Munich International",
    "BCN": "Barcelona International"
}

VALID_AIRLINES = {
    "BA": "British Airways",
    "AF": "Air France",
    "AY": "Finnair",
    "KL": "KLM",
    "SK": "Scandinavian Airlines",
    "TP": "TAP Air Portugal",
    "TK": "Turkish Airlines",
    "W6": "Wizz Air",
    "U2": "easyJet",
    "FR": "Ryanair",
    "A3": "Aegean Airlines",
    "SN": "Brussels Airlines",
    "EK": "Emirates",
    "QR": "Qatar Airways",
    "IB": "Iberia",
    "LH": "Lufthansa"
}

os.chdir(os.path.dirname(__file__))

def load_csv(CSV_chosen):
    """Loads CSV into a local list and returns it."""
    data_list = []
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)  
        for row in csvreader:
            data_list.append(row)
    return data_list


#************************************************************************************************************

#EDIT THE CODE BELOW TO COMPLETE YOUR SUBMISSION

def ask_airport_code():
    """Keeps asking until user enters a valid 3-letter airport code."""
    while True:
        code = input("please enter a three-letter city code:").strip()

        if len(code) != 3:
            print("Wrong code length - please enter a three-letter city code:")
            continue

        code = code.upper()
        if code not in VALID_AIRPORTS:
            print("Unavailable city code - please enter a valid city code")
            continue

        return code


def ask_year():
    """Checks year format and range according to brief."""
    while True:
        year = input("Please enter the year required in the format YYYY:").strip()

        if not year.isdigit() or len(year) != 4:
            print("Wrong data type - please enter a four-digit year value:")
            continue

        year_num = int(year)
        if year_num < 2000 or year_num > 2025:
            print("Out of range - please enter a value from 2000 to 2025:")
            continue

        return year_num


def select_and_load_file():
    """Combines airport code and year to form the CSV filename."""
    code = ask_airport_code()
    year = ask_year()

    selected_data_file = f"{code}{year}.csv"

    print("\n" + "*" * 70)
    print(f"File {selected_data_file} selected - Planes departing {VALID_AIRPORTS[code]} {year}")
    print("*" * 70 + "\n")

    data_list = load_csv(selected_data_file) # now returns list instead of modifying global 
    return selected_data_file, code, year, data_list


def calculate_outcomes(data_list, airport_code, year):
    """Processes data_list and prints all 10 outcomes."""

    total_flights = len(data_list)

    # 2. Flights from Terminal 2
    terminal2_count = 0
    for row in data_list:
        if row[8] == "2":
            terminal2_count += 1

    # 3. Flights under 600 miles
    under_600 = 0
    for row in data_list:
        if row[5].isdigit() and int(row[5]) < 600:
            under_600 += 1

    # 4. Air France flights (AF)
    air_france_count = 0
    for row in data_list:
        flight = row[1]
        if flight.startswith("AF"):
            air_france_count += 1

    # 5. Temps below 15°C
    cold_hours = 0
    for row in data_list:
        weather = row[10]
        # Weather string looks like:  "18°C clear" → first part is temperature
        temp = weather.split("°")[0]
        if temp.isdigit() and int(temp) < 15:
            cold_hours += 1

    # 6. Avg British Airways flights per hour
    ba_per_hour = 0
    ba_count = 0
    for row in data_list:
        if row[1].startswith("BA"):
            ba_count += 1
    ba_per_hour = round(ba_count / 12, 2)

    # 7. BA percentage of total departures
    if total_flights > 0:
        ba_percent = round((ba_count / total_flights) * 100, 2)
    else:
        ba_percent = 0

    # 8. % of Air France flights that are delayed
    af_delayed = 0
    for row in data_list:
        if row[1].startswith("AF"):
            if row[2] != row[3]:  # scheduled vs actual departure
                af_delayed += 1

    if air_france_count > 0:
        af_delay_percent = round((af_delayed / air_france_count) * 100, 2)
    else:
        af_delay_percent = 0

    # 9. Count hours where "rain" appears (once per hour)
    rain_hours = 0
    for row in data_list:
        if "rain" in row[10].lower():
            rain_hours += 1

    # 10. Least common destination(s)
    destination_counts = {}
    for row in data_list:
        dest = row[4]
        if dest not in destination_counts:
            destination_counts[dest] = 0
        destination_counts[dest] += 1

    # Find the minimum count
    min_val = min(destination_counts.values())
    least_common = [VALID_AIRPORTS.get(code, code) for code, cnt in destination_counts.items() if cnt == min_val]

    # Convert airport codes to full names
    full_names = []
    for code in least_common:
        full_names.append(VALID_AIRPORTS.get(code, code))

    # -------------------- PRINT OUTPUT --------------------
    print("*********************************************************************************")
    print(f"File {airport_code}{year}.csv selected - Planes departing {VALID_AIRPORTS[airport_code]} {year}")
    print("*********************************************************************************\n")

    print(f"The total number of flights from this airport was {total_flights}")
    print(f"The total number of flights departing Terminal Two was {terminal2_count}")
    print(f"The total number of departures on flights under 600 miles was {under_600}")
    print(f"There were {air_france_count} Air France flights from this airport")
    print(f"There were {cold_hours} flights departing in temperatures below 15 degrees")
    print(f"There was an average of {ba_per_hour} British Airways flights per hour from this airport")
    print(f"British Airways planes made up {ba_percent}% of all departures")
    print(f"{af_delay_percent}% of Air France departures were delayed")
    print(f"There were {rain_hours} hours in which rain fell")
    print(f"The least common destinations are {full_names}\n")

    # Return values so we can save them in Task C
    return {
        "total": total_flights,
        "terminal2": terminal2_count,
        "under600": under_600,
        "af": air_france_count,
        "cold": cold_hours,
        "ba_hour": ba_per_hour,
        "ba_percent": ba_percent,
        "af_delay": af_delay_percent,
        "rain": rain_hours,
        "least": full_names
    }

def save_results(airport_code, year, results):
    """Appends the 10 outcome values to results.txt in the required format."""
    
    airport_name = VALID_AIRPORTS.get(airport_code, airport_code)
    
    with open("results.txt", "a") as file:   # append mode
        file.write("*************************************************************\n")
        file.write(f"Airport: {airport_name} ({airport_code})   Year: {year}\n")
        file.write("*************************************************************\n")

        file.write(f"1. Total flights: {results['total']}\n")
        file.write(f"2. Terminal 2 flights: {results['terminal2']}\n")
        file.write(f"3. Flights under 600 miles: {results['under600']}\n")
        file.write(f"4. Air France flights: {results['af']}\n")
        file.write(f"5. Flights in temperatures under 15°C: {results['cold']}\n")
        file.write(f"6. Avg British Airways flights per hour: {results['ba_hour']}\n")
        file.write(f"7. British Airways % of all flights: {results['ba_percent']}%\n")
        file.write(f"8. Air France delayed %: {results['af_delay']}%\n")
        file.write(f"9. Rain hours: {results['rain']}\n")
        file.write(f"10. Least common destinations: {results['least']}\n\n")
    print("Results saved to results.txt\n")

def ask_airline_code():
    """Asks user for a valid 2-character airline code."""
    while True:
        code = input("Enter a two-character Airline code to plot a histogram: ").strip().upper()

        if len(code) != 2:
            print("Wrong code length - please enter a two-character code.")
            continue

        if code not in VALID_AIRLINES:
            print("Unavailable Airline code please try again:")
            continue

        return code


def draw_histogram(data_list, airport_code, year):
    """Draws a histogram of number of flights per destination using graphics.py."""

    # Ask user for airline
    airline_code = ask_airline_code()
    airline_name = VALID_AIRLINES[airline_code]
    airport_name = VALID_AIRPORTS[airport_code]

    # Count flights per hour for that airline
    hourly_counts = {h: 0 for h in range(12)}

    for row in data_list:
        if row[1].startswith(airline_code):
            hour = int(row[2][:2])   # scheduled departure hour
            if hour in hourly_counts:
                hourly_counts[hour] += 1


    # Create graphics window
    win = GraphWin("Histogram", 900, 600)
    win.setBackground("white")

    # Title required by brief
    title_text = f"Departures by hour for {airline_name} from {airport_name} {year}"
    title = Text(Point(450, 30), title_text)
    title.setSize(16)
    title.draw(win)

    # Left-side vertical label (matches sample)
    hours_label = Text(Point(50, 300), "Hours\n00:00\nto\n12:00")
    hours_label.setSize(12)
    hours_label.draw(win)

    # Histogram layout
    left_margin = 150
    top_start = 100
    bar_height = 30
    gap = 20


    # Scaling to fit window
    max_count = max(hourly_counts.values()) if max(hourly_counts.values()) > 0 else 1
    scale = 500 / max_count   # max bar height will be 400 px

    y = top_start


    # Draw bars for each hour 0–11
    for hour in range(12):
        count = hourly_counts[hour]
        bar_length = count * scale

        # Hour label at left of bar
        hour_label = Text(Point(left_margin - 40, y + bar_height/2), f"{hour:02d}")
        hour_label.setSize(12)
        hour_label.draw(win)

        # Horizontal bar
        bar = Rectangle(
            Point(left_margin, y),
            Point(left_margin + bar_length, y + bar_height)
        )
        bar.setFill("lightpink")
        bar.draw(win)

        # Count at END of bar
        count_label = Text(Point(left_margin + bar_length + 20, y + bar_height/2), str(count))
        count_label.setSize(12)
        count_label.draw(win)

        y += bar_height + gap

    # Close instruction
    close_msg = Text(Point(480, 580), "Click anywhere to close")
    close_msg.draw(win)

    win.getMouse()
    win.close()


def ask_go_again():
    """Asks the user if they want to run the program again."""
    while True:
        choice = input("Would you like to analyse another file? (Y/N): ").strip().upper()

        if choice == "Y":
            return True
        elif choice == "N":
            return False
        else:
            print("Invalid choice - please enter Y or N:", end="")



if __name__ == "__main__":

    go_again = True

    while go_again:
        # Clear the previous data
        data_list.clear()

        # Task A – input + load CSV
        selected_filename, airport_code, selected_year, data_list = select_and_load_file()
        
        # Task B – calculate outcomes
        results = calculate_outcomes(data_list,airport_code, selected_year)

        # Task C – save to results.txt
        save_results(airport_code, selected_year, results)

        # Task D – histogram
        draw_histogram(data_list,airport_code, selected_year)


        # Task E – ask user to run again
        go_again = ask_go_again()

    print("Thank you for using the Flight Analysis Program.")








