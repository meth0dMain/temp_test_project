### Queries :

To solve all these question I've chosen to use Free Universal Database Tool:  [Dbeaver](https://dbeaver.io/) 
#### 1. The most profitable country for Netflix.

To find the most profitable country for Netflix, we need to calculate the total revenue per country. 
This involves summing up the monthly_revenue for all subscriptions in each country. 
We need to join the subscriptions table with the users table to get the  country information for each user, 
and then sum up the monthly_revenue for each country.

```sql
SELECT
    u.country, 
    SUM(s.monthly_revenue) AS total_revenue
FROM
    subscriptions s
JOIN users u ON s.user_id = u.user_id
GROUP BY u.country
ORDER BY total_revenue DESC
LIMIT 1;
```
<div align="center">
    <img src="images/1st question Dbeaver.png" alt="Logo" width="1000" height="600">
        <h6 align="left">I also checked the data in CSViewer</h6>
    <img src="images/1st question CSViewer.png" alt="Logo" width="900" height="350">
</div>

#### 2.  The most popular packages per country.
To find the most popular subscription package per country, we need to count the number of users subscribed to each 
subscription type within each country, and then identify the subscription type with the highest count for each country. 
This requires a combination of joining the subscriptions and users tables, grouping by country and subscription type, 
and then finding the maximum count for each country.

```sql
SELECT 
    country,
    subscription_type,
    COUNT(subscription_type) AS subscription_count
FROM 
    subscriptions s
JOIN users u ON
    s.user_id = u.user_id
GROUP BY 
    country, subscription_type
ORDER BY 
    country, subscription_count DESC;
```

<div align="center">
    <img src="images/2nd question Dbeaver.png" alt="Logo" width="1000" height="600">
        <h6 align="left">I also checked the data in CSViewer</h6>
    <img src="images/2nd question CSViewer.png" alt="Logo" width="900" height="350">
</div>

#### 3.  Which country has the potential for improving earnings if Netflix starts charging subscribers an additional fee for sharing Netflix households outside their own?

To identify the country with the potential for improving earnings if Netflix starts charging subscribers an 
additional fee for sharing Netflix households outside their own, we need to consider the `household_profile_ind`.
This approach assumes that household_profile_ind can be directly correlated with the potential for additional 
revenue, which is a simplification. In reality, the decision to charge extra fees might also consider the total 
number of subscribers, the average revenue per user, etc.

```sql
SELECT 
    u.country, 
    SUM(p.household_profile_ind) AS potential_revenue_improvement
FROM 
    profiles p
JOIN 
    users u ON p.user_id = u.user_id
GROUP BY 
    u.country
ORDER BY 
    potential_revenue_improvement DESC
LIMIT 1;
```
<div align="center">
    <img src="images/3rd question Dbeaver.png" alt="Logo" width="1000" height="600">
</div>

#### 4.  A report showing the popularity of Movies and Series in different customer segments and the device used to consume, across the different markets the company operates in.

I've chosen the customer segments: `subscription_type`, `device_name` and `age_group`.
We can analyze how different types of customers, classified by their subscription and age, prefer movies or series, 
and which devices they use.
```sql
SELECT
    u.country,
    s.subscription_type,
    d.device_name,
    AVG(v.movies_watched) AS avg_movies_watched,
    AVG(v.series_watched) AS avg_series_watched,
    CASE
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 35 AND 55 THEN '35-55'
        ELSE 'Other'
    END AS age_group
FROM
    users u
JOIN
    subscriptions s ON u.user_id = s.user_id
JOIN
    user_devices ud ON u.user_id = ud.user_id
JOIN
    devices d ON ud.device_id = d.device_id
JOIN
    viewing_activity v ON u.user_id = v.user_id
GROUP BY
    u.country, s.subscription_type, d.device_name
ORDER BY
    u.country, s.subscription_type, d.device_name;
```
This approach gives a multi-dimensional view of content consumption across customer segments, devices, and markets.

<div align="center">
    <img src="images/4th question Dbeaver.png" alt="Logo" width="1000" height="600">
</div>

<h6 align="left">PS. I choose the device_name instead of device_type, can explain during face-to-face interview.</h6>