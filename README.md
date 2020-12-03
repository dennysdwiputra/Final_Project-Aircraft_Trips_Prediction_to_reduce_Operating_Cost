# Final Project - Aircraft Trips Prediction to reduce Operating Cost
How could we predict the average Aircraft trips in this hardest year 2020 during Covid-19 to save the Total Operating Cost ?

# KINDLY CHECK MY PROJECT PRESENTATION BELOW
[CLICK HERE](https://github.com/dennysdwiputra/Final_Project-Aircraft_Trips_Prediction_to_reduce_Operating_Cost/blob/main/Daily%20Aircraft%20Trips%20Prediction%20Machine%20Learning.pdf)

# Background of this Project
>We could see that Corona Virus Disease 19 (Covid-19) in 2020 Obviously create a massive impact for RPKs this year and had beaten the airline Indsutry all around the world.
>Airline Bussines is dinamic bussines, they really depends on the passenger each day, Month, and Year. By the time ,the airline industry getting bigger and bigger, as we could see above , since 1984-2019, RPKs (Revenue Seats Kilometers) in Australia grows very quickly and becomes a promising and highly competitive bussiness. Despite of this, the airline bussines was destroyed because of this pandemic, people should be stayed at home to stop the spread of the virus, many Country take an action to did a Lockdown, All the airport decided to close flight for the safety reason, in the end of third month 2020, this pandemic getting bigger and couldn't be prevented, Cargo Aircraft is the only airplane which could fly in a spesific Country. Every country trying to save their Airline Company, they have to change bussines concept and try to save thier money as much as possible. Several Airline decided to grounded their Aircraft and the other trying hard to survive in this hard situation by change their aircraft configuration from the Passenger aircraft to cargo aircraft, but it is not an easy way to change that ! They have to spend 2.5 to 3 million USD.


# Problem of This Project
> Because of this anomaly year, The Airline Company couldn't use the historical data to predict their passengers to calculate their revenue, their fare, and how to calculate the ticket price from this obscurity. So they have to think more than before, I think we still could predict by we take the flight traffic data as much as possible in this year. But the problem is , We couldn't predict the traffic in future, we still in the anomaly year, many country make their own policy to keep their citizens safe, just like in Australia, several region make territorial quarentine to avoid the spread of the virus, so I think its useless to predict the demand of the passenger in the future and nearly the end of this year, We are still waiting for uncertainly about the safety and healty from this virus.

# Limitation of Machine Learning
>We only take the trafic in 2020.

We dont predict the traffic because the traffic is really depends on the goverment policy in every country.
We just predict in a year 2020 and we only predict the average trips on each day of Year 2020.
The most likely thing that We could do is to reduce the Operational of the Aircraft as efficient as possible, we have to find the new pattern from this hardest year ever.

# Goals
In this project, We would like to predict on the next month, how many flight could be possible in a spesific route based on load factor the month before or the average load factor this year, with the limitation of available seat (On several Airline) because of the safety reason (Social Distancing) to reduce the spread of the virus and the most important think is to restore the customers trust to fly again over the region of Australia or maybe over the country.


# INSIGHT from our Exploratory Data Analysis
1. Since Australia made a desicion to did a lockdown, airline industry got the big impact start from **LOAD FACTOR, DAILY AIRCRAFT TRIPS, PASSENGER TRIPS** drops in 4th Month 2020.
2. 20 City had a **load factor below 0.5 (50%)** which mean this city is not profitable city, because they spend a lot of Opreational Cost, but actually the aircraft just bring the passenger below the 50% from total available seats. If they want to increase the ticket price (keep porfitable), maybe the passenger also could be drecrease because the ticket price is too expensive.
2. **Perth, Newman,Darwin,Melbourne,Emerald, Gladstone** were a highest Total Operating Cost in Australia Domestic Flight, but they had a low load factor which mean they are actaually losing a lot of money. So the have to limit their flight trips to save their money as much as possible.


# Conclusion and Suggestion
## Conclusion :
>After We know about our machine learning performance, we get the conclution that this machine learning :

1. Only predict how many possible times the aircraft could fly in a spesific route , month and load factor based on their traffic before.

2. We couldn't predict the traffic, reveneu because the dataset just provide Monthly traffic, and we know this year we found anomaly with the traffic because of government policy.

3. From this Dataset, we also predict the **scheduled maintenance** for the aircraft in the future, because we predict how many times the aircraft fly and exactly we could predict total landings and total flight hours from the aircraft, total landings and flight hours is one of the standard in aviaton industry to predict the scheduled maintenance.
https://en.wikipedia.org/wiki/Aircraft_maintenance_checks#A_check

## Suggestion :
1. Because of this Model only predict how many times the average from the aircraft could fly in a route, We could boost the traffic based on the prediction with a special promo like AirAsia Indonesia, they give a special promo just pay Rp.1.500.000, we could fly unlimited in 6 month in all destination in Indonesia which airasia provided.

2. We could predict more accurate if we get the daily traffic, so the decission will be better than this machine learning.

3. The Airline should consider about the ticket price after get the prediction of this model. 
