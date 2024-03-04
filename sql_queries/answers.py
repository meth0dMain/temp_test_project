# 1. The most profitable country for Netflix.
MOST_PROFITABLE_COUNTRY = """
SELECT
    u.country, 
    SUM(s.monthly_revenue) AS total_revenue
FROM
    subscriptions s
JOIN users u ON s.user_id = u.user_id
GROUP BY u.country
ORDER BY total_revenue DESC
LIMIT 1;
"""
# 2. The most popular packages per country
MOST_POPULAR_PACKAGES_PER_COUNTRY_WITH_NUMBERS = """
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
"""
# 2. The most popular packages per country
MOST_POPULAR_PACKAGES_PER_COUNTRY_LITE = """
WITH SubscriptionCounts AS (
    SELECT
        u.country,
        s.subscription_type,
        COUNT(*) AS subscription_count,
        RANK() OVER (PARTITION BY u.country ORDER BY COUNT(*) DESC) as rank
    FROM subscriptions s
    JOIN users u ON s.user_id = u.user_id
    GROUP BY u.country, s.subscription_type
)
SELECT country, subscription_type
FROM SubscriptionCounts
WHERE rank = 1;
"""
# 3. Which country has the potential for improving earnings if Netflix starts charging subscribers
# an additional fee for sharing Netflix households outside their own?
POTENTIAL_FOR_IMPROVING_EARNINGS = """
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
"""
# 4. A report showing the popularity of Movies and Series in different customer segments and
# the device used to consume, across the different markets the company operates in.
REPORT_CUSTOMER_SEGMENTS = """
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
"""
