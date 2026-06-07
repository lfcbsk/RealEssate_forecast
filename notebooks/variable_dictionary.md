# Variable Dictionary - Real Estate Data

## Table of Contents
- [Pre-owned House Transactions](#pre-owned-house-transactions)
- [New House Transactions](#new-house-transactions)
- [Land Transactions](#land-transactions)
- [Sector POI (Points of Interest)](#sector-poi-points-of-interest)
- [City Search Index](#city-search-index)
- [City Indicators](#city-indicators)

---

## Pre-owned House Transactions

### Direct Sector Data (`pre_owned_house_transactions.csv`)

| Variable | Description | Unit |
|----------|-------------|------|
| `month` | The month of the transaction | Date |
| `sector` | The specific geographic sector where the transaction occurred | Categorical |
| `area_pre_owned_house_transactions` | Total area of pre-owned house transactions | m² |
| `amount_pre_owned_house_transactions` | Total monetary value of pre-owned house transactions | 10,000 yuan |
| `num_pre_owned_house_transactions` | Total number of pre-owned house transactions | Count |
| `price_pre_owned_house_transactions` | Average price per square meter of pre-owned house transactions | yuan/m² |

### Nearby Sectors Data (`pre_owned_house_transactions_nearby_sectors.csv`)

| Variable | Description | Unit |
|----------|-------------|------|
| `month` | The month of the transaction | Date |
| `sector` | The specific geographic sector of interest | Categorical |
| `area_pre_owned_house_transactions_nearby_sectors` | Total area of pre-owned house transactions in nearby sectors | m² |
| `amount_pre_owned_house_transactions_nearby_sectors` | Total monetary value of pre-owned house transactions in nearby sectors | 10,000 yuan |
| `num_pre_owned_house_transactions_nearby_sectors` | Total number of pre-owned house transactions in nearby sectors | Count |
| `price_pre_owned_house_transactions_nearby_sectors` | Average price per square meter of pre-owned house transactions in nearby sectors | yuan/m² |

---

## New House Transactions

### Direct Sector Data (`new_house_transactions.csv`)

#### Transaction Metrics
| Variable | Description | Unit |
|----------|-------------|------|
| `month` | The month of the transaction | Date |
| `sector` | The specific geographic sector where the new house transaction occurred | Categorical |
| `num_new_house_transactions` | Total number of new house transactions | Count |
| `area_new_house_transactions` | Total area of new house transactions | m² |
| `price_new_house_transactions` | Average price per square meter of new house transactions | yuan/m² |
| `amount_new_house_transactions` | Total monetary value of new house transactions | 10,000 yuan |

#### Unit-level Metrics
| Variable | Description | Unit |
|----------|-------------|------|
| `area_per_unit_new_house_transactions` | Average area per new house transaction unit | m²/unit |
| `total_price_per_unit_new_house_transactions` | Average total price per new house transaction unit | 10,000 yuan/unit |

#### Inventory Metrics
| Variable | Description | Unit |
|----------|-------------|------|
| `num_new_house_available_for_sale` | Total number of new houses available for sale | Count |
| `area_new_house_available_for_sale` | Total area of new houses available for sale | m² |
| `period_new_house_sell_through` | Estimated time to sell all available new houses | Months |

### Nearby Sectors Data (`new_house_transactions_nearby_sectors.csv`)

#### Transaction Metrics
| Variable | Description | Unit |
|----------|-------------|------|
| `month` | The month of the transaction | Date |
| `sector` | The specific geographic sector of interest | Categorical |
| `num_new_house_transactions_nearby_sectors` | Total number of new house transactions in nearby sectors | Count |
| `area_new_house_transactions_nearby_sectors` | Total area of new house transactions in nearby sectors | m² |
| `price_new_house_transactions_nearby_sectors` | Average price per square meter of new house transactions in nearby sectors | yuan/m² |
| `amount_new_house_transactions_nearby_sectors` | Total monetary value of new house transactions in nearby sectors | 10,000 yuan |

#### Unit-level Metrics
| Variable | Description | Unit |
|----------|-------------|------|
| `area_per_unit_new_house_transactions_nearby_sectors` | Average area per new house transaction unit in nearby sectors | m²/unit |
| `total_price_per_unit_new_house_transactions_nearby_sectors` | Average total price per new house transaction unit in nearby sectors | 10,000 yuan/unit |

#### Inventory Metrics
| Variable | Description | Unit |
|----------|-------------|------|
| `num_new_house_available_for_sale_nearby_sectors` | Total number of new houses available for sale in nearby sectors | Count |
| `area_new_house_available_for_sale_nearby_sectors` | Total area of new houses available for sale in nearby sectors | m² |
| `period_new_house_sell_through_nearby_sectors` | Estimated time to sell all available new houses in nearby sectors | Months |

---

## Land Transactions

### Direct Sector Data (`land_transactions.csv`)

| Variable | Description | Unit |
|----------|-------------|------|
| `month` | The month of the transaction | Date |
| `sector` | The specific geographic sector where the land transaction occurred | Categorical |
| `num_land_transactions` | Total number of land transactions | Count |
| `construction_area` | Total area of land designated for construction | m² |
| `planned_building_area` | Total planned building area on the transacted land | m² |
| `transaction_amount` | Total monetary value of land transactions | 10,000 yuan |

### Nearby Sectors Data (`land_transactions_nearby_sectors.csv`)

| Variable | Description | Unit |
|----------|-------------|------|
| `month` | The month of the transaction | Date |
| `sector` | The specific geographic sector of interest | Categorical |
| `num_land_transactions_nearby_sectors` | Total number of land transactions in nearby sectors | Count |
| `construction_area_nearby_sectors` | Total area of land designated for construction in nearby sectors | m² |
| `planned_building_area_nearby_sectors` | Total planned building area on transacted land in nearby sectors | m² |
| `transaction_amount_nearby_sectors` | Total monetary value of land transactions in nearby sectors | 10,000 yuan |

---

## Sector POI (Points of Interest)

### Basic Sector Information

| Variable | Description | Type |
|----------|-------------|------|
| `sector` | The specific geographic sector | Categorical |
| `sector_coverage` | Geographical extent or area covered by the sector | Numeric |

### Population Metrics (Absolute)

| Variable | Description | Unit |
|----------|-------------|------|
| `population_scale` | General size of the population within the sector | Numeric |
| `resident_population` | Number of people residing in the sector | Count |
| `office_population` | Number of people working in offices within the sector | Count |

### Population Metrics (Density)

| Variable | Description | Type |
|----------|-------------|------|
| `population_scale_dense` | Density of the population scale within the sector | Density |
| `resident_population_dense` | Density of the resident population within the sector | Density |
| `office_population_dense` | Density of the office population within the sector | Density |

### Land Use - Absolute

| Variable | Description | Type |
|----------|-------------|------|
| `residential_area` | Presence or extent of residential zones within the sector | Numeric |
| `office_building` | Presence or extent of office buildings within the sector | Numeric |
| `commercial_area` | Presence or extent of commercial zones within the sector | Numeric |

### Land Use - Density

| Variable | Description | Type |
|----------|-------------|------|
| `residential_area_dense` | Density of residential areas within the sector | Density |
| `office_building_dense` | Density of office buildings within the sector | Density |
| `commercial_area_dense` | Density of commercial areas within the sector | Density |

### Retail & Commercial (Absolute)

| Variable | Description | Unit |
|----------|-------------|------|
| `number_of_shops` | Total count of shops in the sector | Count |
| `rentable_shops` | Number of shops available for rent | Count |
| `catering` | Number or density of catering establishments | Count |
| `retail` | Number or density of retail establishments | Count |
| `hotel` | Number or density of hotel establishments | Count |

### Retail & Commercial (Density)

| Variable | Description | Type |
|----------|-------------|------|
| `number_of_shops_dense` | Density of shops within the sector | Density |
| `rentable_shops_dense` | Density of rentable shops | Density |
| `catering_dense` | Density of catering establishments | Density |
| `retail_dense` | Density of retail establishments | Density |
| `hotel_dense` | Density of hotel establishments | Density |

### Store Types (Absolute)

| Variable | Description | Unit |
|----------|-------------|------|
| `number_of_leisure_and_entertainment_stores` | Count of leisure and entertainment stores | Count |
| `number_of_other_stores` | Count of miscellaneous other stores | Count |
| `number_of_other_anchor_stores` | Count of other major or anchor stores | Count |
| `number_of_home_appliance_stores` | Count of home appliance stores | Count |
| `number_of_skincare_cosmetics_stores` | Count of skincare and cosmetics stores | Count |
| `number_of_fashion_stores` | Count of fashion stores | Count |
| `number_of_service_stores` | Count of service-oriented stores | Count |
| `number_of_jewelry_stores` | Count of jewelry stores | Count |
| `number_of_lifestyle_leisure_stores` | Count of lifestyle and leisure stores | Count |
| `number_of_supermarket_convenience_stores` | Count of supermarkets and convenience stores | Count |
| `number_of_catering_food_stores` | Count of catering and food stores | Count |

### Store Types (Density)

| Variable | Description | Type |
|----------|-------------|------|
| `leisure_entertainment_stores_dense` | Density of leisure and entertainment stores | Density |
| `other_stores_dense` | Density of miscellaneous other stores | Density |
| `other_anchor_stores_dense` | Density of other major or anchor stores | Density |
| `home_appliance_stores_dense` | Density of home appliance stores | Density |
| `skincare_cosmetics_stores_dense` | Density of skincare and cosmetics stores | Density |
| `fashion_stores_dense` | Density of fashion stores | Density |
| `service_stores_dense` | Density of service-oriented stores | Density |
| `jewelry_stores_dense` | Density of jewelry stores | Density |
| `lifestyle_leisure_stores_dense` | Density of lifestyle and leisure stores | Density |
| `supermarket_convenience_stores_dense` | Density of supermarkets and convenience stores | Density |
| `catering_food_stores_dense` | Density of catering and food stores | Density |

### Commercial Building Types (Absolute)

| Variable | Description | Unit |
|----------|-------------|------|
| `number_of_residential_commercial` | Count of commercial establishments within residential areas | Count |
| `number_of_office_building_commercial` | Count of commercial establishments within office buildings | Count |
| `number_of_commercial_buildings` | Count of dedicated commercial buildings | Count |
| `number_of_hypermarkets` | Count of hypermarkets | Count |
| `number_of_department_stores` | Count of department stores | Count |
| `number_of_shopping_centers` | Count of shopping centers | Count |
| `number_of_hotel_commercial` | Count of commercial establishments within hotels | Count |

### Commercial Building Types (Density)

| Variable | Description | Type |
|----------|-------------|------|
| `residential_commercial_dense` | Density of commercial establishments within residential areas | Density |
| `office_building_commercial_dense` | Density of commercial establishments within office buildings | Density |
| `commercial_buildings_dense` | Density of dedicated commercial buildings | Density |
| `hypermarkets_dense` | Density of hypermarkets | Density |
| `department_stores_dense` | Density of department stores | Density |
| `shopping_centers_dense` | Density of shopping centers | Density |
| `hotel_commercial_dense` | Density of commercial establishments within hotels | Density |

### Shopping Mall Types (Absolute)

| Variable | Description | Unit |
|----------|-------------|------|
| `number_of_third_tier_shopping_malls_in_business_district` | Count of third-tier shopping malls within the business district | Count |
| `number_of_second_tier_shopping_malls_in_business_district` | Count of second-tier shopping malls within the business district | Count |
| `number_of_city_winner_malls` | Count of high-performing "city winner" malls | Count |
| `number_of_shopping_malls_with_street_facing_shops` | Count of shopping malls featuring street-facing shops | Count |
| `number_of_unranked_malls` | Count of shopping malls without a specific ranking | Count |
| `number_of_community_malls` | Count of community-focused malls | Count |
| `number_of_community_winner_malls` | Count of high-performing "community winner" malls | Count |
| `number_of_key_focus_malls` | Count of shopping malls identified for key focus | Count |

### Shopping Mall Types (Density)

| Variable | Description | Type |
|----------|-------------|------|
| `third_tier_shopping_malls_in_business_district_dense` | Density of third-tier shopping malls within the business district | Density |
| `second_tier_shopping_malls_in_business_district_dense` | Density of second-tier shopping malls within the business district | Density |
| `city_winner_malls_dense` | Density of high-performing "city winner" malls | Density |
| `shopping_malls_with_street_facing_shops_dense` | Density of shopping malls featuring street-facing shops | Density |
| `unranked_malls_dense` | Density of shopping malls without a specific ranking | Density |
| `community_malls_dense` | Density of community-focused malls | Density |
| `community_winner_malls_dense` | Density of high-performing "community winner" malls | Density |
| `key_focus_malls_dense` | Density of shopping malls identified for key focus | Density |

### Transportation Infrastructure (Absolute)

| Variable | Description | Unit |
|----------|-------------|------|
| `transportation_station` | Number or density of transportation stations | Count |
| `bus_station_cnt` | Count of bus stations | Count |
| `subway_station_cnt` | Count of subway stations | Count |
| `transportation_facilities_service_bus_station` | Presence or density of bus stations | Numeric |
| `transportation_facilities_service_subway_station` | Presence or density of subway stations | Numeric |
| `transportation_facilities_service_airport_related` | Presence or density of airport-related facilities | Numeric |
| `transportation_facilities_service_port_terminal` | Presence or density of port or terminal facilities | Numeric |
| `transportation_facilities_service_train_station` | Presence or density of train stations | Numeric |
| `transportation_facilities_service_light_rail_station` | Presence or density of light rail stations | Numeric |
| `transportation_facilities_service_long_distance_bus_station` | Presence or density of long-distance bus stations | Numeric |

### Transportation Infrastructure (Density)

| Variable | Description | Type |
|----------|-------------|------|
| `transportation_station_dense` | Density of transportation stations | Density |
| `bus_station_cnt_dense` | Density of bus stations | Density |
| `subway_station_cnt_dense` | Density of subway stations | Density |
| `transportation_facilities_service_bus_station_dense` | Density of bus stations | Density |
| `transportation_facilities_service_subway_station_dense` | Density of subway stations | Density |
| `transportation_facilities_service_airport_related_dense` | Density of airport-related facilities | Density |
| `transportation_facilities_service_port_terminal_dense` | Density of port or terminal facilities | Density |
| `transportation_facilities_service_train_station_dense` | Density of train stations | Density |
| `transportation_facilities_service_light_rail_station_dense` | Density of light rail stations | Density |
| `transportation_facilities_service_long_distance_bus_station_dense` | Density of long-distance bus stations | Density |

### Education Facilities (Absolute)

| Variable | Description | Unit |
|----------|-------------|------|
| `education` | Number or density of educational facilities | Count |
| `education_training_school_education_middle_school` | Number or density of middle schools | Count |
| `education_training_school_education_primary_school` | Number or density of primary schools | Count |
| `education_training_school_education_kindergarten` | Number or density of kindergartens | Count |
| `education_training_school_education_research_institution` | Number or density of research institutions | Count |

### Education Facilities (Density)

| Variable | Description | Type |
|----------|-------------|------|
| `education_dense` | Density of educational facilities | Density |
| `education_training_school_education_middle_school_dense` | Density of middle schools | Density |
| `education_training_school_education_primary_school_dense` | Density of primary schools | Density |
| `education_training_school_education_kindergarten_dense` | Density of kindergartens | Density |
| `education_training_school_education_research_institution_dense` | Density of research institutions | Density |

### Medical & Health Facilities (Absolute)

| Variable | Description | Unit |
|----------|-------------|------|
| `medical_health` | Number or density of general medical and health facilities | Count |
| `medical_health_specialty_hospital` | Number or density of specialty hospitals | Count |
| `medical_health_tcm_hospital` | Number or density of Traditional Chinese Medicine (TCM) hospitals | Count |
| `medical_health_physical_examination_institution` | Number or density of physical examination institutions | Count |
| `medical_health_veterinary_station` | Number or density of veterinary stations | Count |
| `medical_health_pharmaceutical_healthcare` | Number or density of pharmaceutical healthcare providers | Count |
| `medical_health_rehabilitation_institution` | Number or density of rehabilitation institutions | Count |
| `medical_health_first_aid_center` | Number or density of first aid centers | Count |
| `medical_health_blood_donation_station` | Number or density of blood donation stations | Count |
| `medical_health_disease_prevention_institution` | Number or density of disease prevention institutions | Count |
| `medical_health_general_hospital` | Number or density of general hospitals | Count |
| `medical_health_clinic` | Number or density of clinics | Count |

### Medical & Health Facilities (Density)

| Variable | Description | Type |
|----------|-------------|------|
| `medical_health_dense` | Density of general medical and health facilities | Density |
| `medical_health_specialty_hospital_dense` | Density of specialty hospitals | Density |
| `medical_health_tcm_hospital_dense` | Density of Traditional Chinese Medicine (TCM) hospitals | Density |
| `medical_health_physical_examination_institution_dense` | Density of physical examination institutions | Density |
| `medical_health_veterinary_station_dense` | Density of veterinary stations | Density |
| `medical_health_pharmaceutical_healthcare_dense` | Density of pharmaceutical healthcare providers | Density |
| `medical_health_rehabilitation_institution_dense` | Density of rehabilitation institutions | Density |
| `medical_health_first_aid_center_dense` | Density of first aid centers | Density |
| `medical_health_blood_donation_station_dense` | Density of blood donation stations | Density |
| `medical_health_disease_prevention_institution_dense` | Density of disease prevention institutions | Density |
| `medical_health_general_hospital_dense` | Density of general hospitals | Density |
| `medical_health_clinic_dense` | Density of clinics | Density |

### Leisure & Entertainment (Absolute)

| Variable | Description | Unit |
|----------|-------------|------|
| `leisure_and_entertainment` | Number or density of leisure and entertainment venues | Count |
| `leisure_entertainment_entertainment_venue_game_arcade` | Number or density of game arcades | Count |
| `leisure_entertainment_entertainment_venue_party_house` | Number or density of party houses | Count |
| `leisure_entertainment_cultural_venue_cultural_palace` | Number or density of cultural palaces | Count |

### Leisure & Entertainment (Density)

| Variable | Description | Type |
|----------|-------------|------|
| `leisure_and_entertainment_dense` | Density of leisure and entertainment venues | Density |
| `leisure_entertainment_entertainment_venue_game_arcade_dense` | Density of game arcades | Density |
| `leisure_entertainment_entertainment_venue_party_house_dense` | Density of party houses | Density |
| `leisure_entertainment_cultural_venue_cultural_palace_dense` | Density of cultural palaces | Density |

### Office & Industrial (Absolute & Density)

| Variable | Description | Type |
|----------|-------------|------|
| `office_building_industrial_building_industrial_building` | Number or density of industrial buildings used as office spaces | Count |
| `office_building_industrial_building_industrial_building_dense` | Density of industrial buildings used as office spaces | Density |

### Price Information

| Variable | Description | Unit |
|----------|-------------|------|
| `surrounding_housing_average_price` | Average price of housing in the surrounding area | yuan/m² |
| `surrounding_shop_average_rent` | Average rent of shops in the surrounding area | yuan |

---

## City Search Index

| Variable | Description | Type |
|----------|-------------|------|
| `month` | The month the search data was recorded | Date |
| `keyword` | The specific search term | Text |
| `source` | The origin or platform of the search data | Categorical |
| `search_volume` | The total number of searches for the keyword | Count |

---

## City Indicators

### Basic Demographics

#### Population Structure
| Variable | Description | Unit |
|----------|-------------|------|
| `city_indicator_data_year` | The year to which the city indicator data pertains | Year |
| `year_end_registered_population_10k` | Registered population at year-end | 10,000 persons |
| `year_end_resident_population_10k` | Permanent resident population at year-end | 10,000 persons |
| `national_year_end_total_population_10k` | National total population at year-end | 10,000 persons |
| `total_households_10k` | Total number of households | 10,000 households |
| `resident_registered_ratio` | Ratio of permanent residents to registered population | Ratio |
| `national_population_share` | City's share of the national population | Percentage |

#### Age Distribution (Absolute)
| Variable | Description | Unit |
|----------|-------------|------|
| `under_18_10k` | Population under 18 years old | 10,000 persons |
| `18_60_years_10k` | Population aged 18 to 60 years old | 10,000 persons |
| `over_60_years_10k` | Population over 60 years old | 10,000 persons |
| `total` | Total population count | Persons |

#### Age Distribution (Percentage)
| Variable | Description | Unit |
|----------|-------------|------|
| `under_18_percent` | Percentage of population under 18 years old | % |
| `18_60_years_percent` | Percentage of population aged 18 to 60 years old | % |
| `over_60_years_percent` | Percentage of population over 60 years old | % |

### Employment

#### Employment Overview
| Variable | Description | Unit |
|----------|-------------|------|
| `year_end_total_employed_population_10k` | Total employed population at year-end | 10,000 persons |
| `year_end_urban_non_private_employees_10k` | Number of urban non-private unit employees at year-end | 10,000 persons |
| `private_individual_and_other_employees_10k` | Number of private, individual, and other employees | 10,000 persons |
| `private_individual_ratio` | Proportion of private and individual employees | Ratio |
| `employed_population` | Total number of employed individuals | Persons |

#### Employment by Industry (Percentage)
| Variable | Description | Unit |
|----------|-------------|------|
| `primary_industry_percent` | Percentage of employed population in primary industry | % |
| `secondary_industry_percent` | Percentage of employed population in secondary industry | % |
| `tertiary_industry_percent` | Percentage of employed population in tertiary industry | % |
| `white_collar_service_vs_blue_collar_manufacturing_ratio` | Ratio of white-collar (service) to blue-collar (manufacturing) population | Ratio |

### Economic Indicators

#### GDP Metrics
| Variable | Description | Unit |
|----------|-------------|------|
| `gdp_100m` | Gross Domestic Product (GDP) | 100 million yuan |
| `primary_industry_100m` | Output value of primary industry | 100 million yuan |
| `secondary_industry_100m` | Output value of secondary industry | 100 million yuan |
| `tertiary_industry_100m` | Output value of tertiary industry | 100 million yuan |
| `gdp_per_capita_yuan` | GDP per capita | yuan |
| `national_gdp_100m` | National GDP | 100 million yuan |

#### Economic Structure
| Variable | Description | Type |
|----------|-------------|------|
| `national_economic_primacy` | City's economic dominance compared to the nation | Index |
| `gdp_population_ratio` | Ratio of city's GDP primacy to its national population share | Ratio |
| `secondary_industry_development_gdp_share` | Share of secondary industry in GDP | % |
| `tertiary_industry_development_gdp_share` | Share of tertiary industry in GDP | % |

### Government Finance

| Variable | Description | Unit |
|----------|-------------|------|
| `general_public_budget_revenue_100m` | General public budget revenue | 100 million yuan |
| `general_public_budget_expenditure_100m` | General public budget expenditure | 100 million yuan |
| `personal_income_tax_100m` | Personal income tax collected | 100 million yuan |
| `per_capita_personal_income_tax_yuan` | Per capita personal income tax | yuan |
| `science_expenditure_10k` | Expenditure on science | 10,000 yuan |
| `education_expenditure_10k` | Expenditure on education | 10,000 yuan |

### Consumer & Retail

| Variable | Description | Unit |
|----------|-------------|------|
| `total_retail_sales_of_consumer_goods_100m` | Total retail sales of consumer goods | 100 million yuan |
| `retail_sales_growth_rate` | Growth rate of retail sales | % |
| `urban_consumer_price_index_previous_year_100` | Urban consumer price index (previous year = 100) | Index |

### Income & Living Standards

#### Income Metrics
| Variable | Description | Unit |
|----------|-------------|------|
| `annual_average_wage_urban_non_private_employees_yuan` | Annual average wage of urban non-private unit employees | yuan |
| `annual_average_wage_urban_non_private_on_duty_employees_yuan` | Annual average wage of urban non-private on-duty employees | yuan |
| `per_capita_disposable_income_absolute_yuan` | Absolute value of per capita disposable income | yuan |
| `per_capita_disposable_income_index_previous_year_100` | Per capita disposable income index (previous year = 100) | Index |

#### Living Standards
| Variable | Description | Unit |
|----------|-------------|------|
| `engel_coefficient` | Proportion of income spent on food | Coefficient |
| `per_capita_housing_area_sqm` | Per capita housing area | m² |

### Education Infrastructure

| Variable | Description | Unit |
|----------|-------------|------|
| `number_of_universities` | Total count of universities and colleges | Count |
| `university_students_10k` | Number of university students | 10,000 students |
| `number_of_middle_schools` | Total count of middle schools | Count |
| `middle_school_students_10k` | Number of middle school students | 10,000 students |
| `number_of_primary_schools` | Total count of primary schools | Count |
| `primary_school_students_10k` | Number of primary school students | 10,000 students |
| `number_of_kindergartens` | Total count of kindergartens | Count |
| `kindergarten_students_10k` | Number of kindergarten students | 10,000 students |

### Healthcare Infrastructure

| Variable | Description | Unit |
|----------|-------------|------|
| `hospitals_health_centers` | Total count of hospitals and health centers | Count |
| `hospital_beds_10k` | Number of hospital beds | 10,000 beds |
| `health_technical_personnel_10k` | Number of health technical personnel | 10,000 persons |
| `doctors_10k` | Number of doctors | 10,000 persons |

### Transportation Infrastructure

| Variable | Description | Unit |
|----------|-------------|------|
| `road_length_km` | Total length of roads | km |
| `road_area_10k_sqm` | Total area of roads | 10,000 m² |
| `per_capita_urban_road_area_sqm` | Per capita urban road area | m² |
| `number_of_operating_bus_lines` | Total count of operating bus lines | Count |
| `operating_bus_line_length_km` | Total length of operating bus lines | km |

### Digital Infrastructure

| Variable | Description | Unit |
|----------|-------------|------|
| `internet_broadband_access_subscribers_10k` | Number of internet broadband access subscribers | 10,000 subscribers |
| `internet_broadband_access_ratio` | Ratio of internet broadband access | Ratio |

### Industrial & Investment

#### Industrial Enterprises
| Variable | Description | Unit |
|----------|-------------|------|
| `number_of_industrial_enterprises_above_designated_size` | Count of industrial enterprises above designated size | Count |
| `total_current_assets_10k` | Total current assets | 10,000 yuan |
| `total_fixed_assets_10k` | Total fixed assets | 10,000 yuan |
| `main_business_taxes_and_surcharges_10k` | Main business taxes and surcharges | 10,000 yuan |

#### Investment
| Variable | Description | Unit |
|----------|-------------|------|
| `total_fixed_asset_investment_10k` | Total fixed asset investment | 10,000 yuan |
| `real_estate_development_investment_completed_10k` | Completed real estate development investment | 10,000 yuan |
| `residential_development_investment_completed_10k` | Completed residential development investment | 10,000 yuan |

---



## Notes
- All monetary values in **yuan** unless specified otherwise (10,000 yuan or 100 million yuan)
- Population metrics typically in **10,000 persons**
- Area metrics in **square meters (m²)** or **square kilometers (km²)**
- Many variables have both **absolute** and **density** versions for sector analysis
