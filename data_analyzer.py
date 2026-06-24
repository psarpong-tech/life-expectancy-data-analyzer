# I added country-specific life expectancy statistics with error validation for invalid inputs, and reprompt user till they enter correct input.
# I added a code to identify the country with the largest life expectancy drop over a 5-year period.

year_interested = int(input("Enter the year of interest (enter 0 to quit): ")) 
while year_interested != 0:
    # For highest overall life expectancy
    highest_life_expectancy = float("-inf") 
    highest_country = ""
    highest_year = 0
    
    # For lowest overall life expectancy
    lowest_life_expectancy = float("inf")
    lowest_country = ""
    lowest_year = 0
    
    # For year of interest statistics
    overall_life_expectancy_total = 0
    year_count = 0
    year_highest_life_expectancy = float("-inf")
    year_highest_country = ""
    year_lowest_life_expectancy = float("inf")
    year_lowest_country = ""
    
    # For country tracking and year-over-year changes
    country_name_list = []
    country_year_list = []
    country_life_expectancy_list = []
    largest_drop = 0
    drop_country = ""
    drop_year = 0

    # Validate year input and re-prompt for input till user types a year found in dataset
    year_valid = False
    while not year_valid and year_interested != 0:
        with open("life-expectancy.csv") as file:

            next(file)

            country_year_list = []
            
            for line in file:
                new_line = line.strip()
                parts = new_line.split(",")
                year = int(parts[2])
                country_year_list.append(year)
        
        if year_interested in country_year_list:
            year_valid = True
        else:
            print(f"Invalid input: {year_interested} is not in the dataset.")
            year_interested = int(input("Enter a year of interest from the dataset (enter 0 to quit): "))

    if year_interested != 0:
        with open("life-expectancy.csv") as file:
            next(file) 

            for line in file:
               
                data = line.strip()

                parts = data.split(",")
                entity = parts[0]
                code = parts[1]
                year = int(parts[2])
                life_expectancy = float(parts[3])
                
                # Store all country data by year for country-specific queries
                country_name_list.append(entity)
                country_year_list.append(year)
                country_life_expectancy_list.append(life_expectancy)


                # Track highest life expectancy overall
                if life_expectancy > highest_life_expectancy:
                    highest_life_expectancy = life_expectancy
                    highest_country = entity
                    highest_year = year

                # Track lowest life expectancy overall
                if life_expectancy < lowest_life_expectancy:
                    lowest_life_expectancy = life_expectancy
                    lowest_country = entity
                    lowest_year = year

                # Calculate statistics for the year of interest
                if year_interested == year:
                    overall_life_expectancy_total += life_expectancy
                    year_count += 1

                    # Track highest life expectancy for year of interest
                    if life_expectancy > year_highest_life_expectancy:
                        year_highest_life_expectancy = life_expectancy
                        year_highest_country = entity

                    # Track lowest life expectancy for year of interest
                    if life_expectancy < year_lowest_life_expectancy:
                        year_lowest_life_expectancy = life_expectancy
                        year_lowest_country = entity
        
        # Calculate largest drop in life expectancy from one year to the 5th year
        country_count = 0
        while country_count < len(country_year_list) - 5 and country_count + 5 < len(country_life_expectancy_list):
            next_country_count = country_count + 5
            
            current_country = country_name_list[country_count]
            current_year = country_year_list[country_count]
            current_life_expectancy = country_life_expectancy_list[country_count]
            
            fifth_year_life_expectancy = country_life_expectancy_list[next_country_count]
            
            drop = current_life_expectancy - fifth_year_life_expectancy
            
            if drop > largest_drop:
                largest_drop = drop
                drop_country = current_country
                drop_year = current_year
            
            country_count = country_count + 1

        average_life_expectancy = overall_life_expectancy_total / year_count

        print()
        print(f"The overall max life expectancy is: {highest_life_expectancy} from {highest_country} in {highest_year}")
        print(f"The overall min life expectancy is: {lowest_life_expectancy} from {lowest_country} in {lowest_year}")

        print()
        print(f"For the year {year_interested}:")
        print(f"The average life expectancy across all countries was {average_life_expectancy:.2f}")
        print(f"The max life expectancy was in {year_highest_country} with {year_highest_life_expectancy}")
        print(f"The min life expectancy was in {year_lowest_country} with {year_lowest_life_expectancy}")
        
        print()
        print(f"The largest drop in life expectancy was in {drop_country} from {drop_year} to {drop_year + 5} with a drop of {largest_drop:.2f}")
        
        # Allows user to enter interested countries for their statistics until they enter 0
        print()
        country_interested = input("Enter a country name to see its statistics (enter 0 to move to next year): ")
        while country_interested != "0":
           
            country_interested_lower = country_interested.lower()
            
            country_name_list_lower = [country.lower() for country in country_name_list]
            
            # Validate country input and re-prompt for input till the user enters country found in dataset
            while country_interested != "0" and country_interested_lower not in country_name_list_lower:
                print(f"Invalid input: {country_interested} is not found in the dataset.")
                country_interested = input("Enter a country name from the dataset (enter 0 to move to next year): ")
                country_interested_lower = country_interested.lower()
            
            # Calculates and displays the minimum, maximum, and average life expectancy for country of interest
            if country_interested != "0":
                minimum_life_expectancy = float("inf")
                maximum_life_expectancy = float("-inf")
                total_life_expectancy = 0
                country_count = 0
                
                for i in range(len(country_name_list)):
                    
                    current_country_lower = country_name_list[i].lower()
                    
                    if current_country_lower == country_interested_lower:
                        life_expectancy = country_life_expectancy_list[i]
                        
                        if life_expectancy < minimum_life_expectancy:
                            minimum_life_expectancy = life_expectancy
                        
                        if life_expectancy > maximum_life_expectancy:
                            maximum_life_expectancy = life_expectancy
                        
                        total_life_expectancy += life_expectancy
                        country_count += 1
                
                average_life_expectancy = total_life_expectancy / country_count
                
                print()
                print(f"For the country {country_interested}:")
                print(f"The minimum life expectancy is: {minimum_life_expectancy:.2f}")
                print(f"The maximum life expectancy is: {maximum_life_expectancy:.2f}")
                print(f"The average life expectancy is: {average_life_expectancy:.2f}")
            
            # Prompt for the next country of interest
            if country_interested != "0":
                country_interested = input("Enter a country name to see its statistics (enter 0 to move to next year): ")

    # Prompt for the next year of interest
    year_interested = int(input("Enter the year of interest (enter 0 to quit): "))