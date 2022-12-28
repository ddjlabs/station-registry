# Data Model Design
Last Updated 12-28-2022

## Station Registry Data Model
NOTE: Tables will be prefixed with stationregistry_

```mermaid
erDiagram
    Stations ||--o{ StationEntry : references
    StationStatus ||--|{ Stations : assigned
    Stations ||--o{ StationExtension: references
    Stations {
        int station_id pk "Internal Key"
        string station_url pk "Unique Key"
        int station_status_id fk "linked to StationStatus"
        boolean valid_url_yn "Valid URL"
        decimal latitude
        decimal longitude
        string location_city
        string location_province
        string location_country
        string description
        string station_type
        string station_model
        string weewx_info
        string python_info
        string platform_info
        string config_path
        string entry_path
        string last_ip_address
        datetime register_dt
        datetime last_entry_dt
        datetime last_url_check_dt
        datetime site_profile_image_gen_dt
        string station_site_image
    }
    StationEntry {
        int entry_id pk "Internal Key"
        datetime entry_dt
        int station_id fk "Linked to Stations"
        string station_url pk "Unique Key"
        decimal latitude
        decimal longitude
        string location_city
        string location_province
        string location_country
        string description
        string station_type
        string station_model
        string weewx_info
        string python_info
        string platform_info
        string config_path
        string entry_path
        string last_ip_address
    }
    StationExtension{
        int station_extension_id pk
        int station_id fk "Linked to Stations"
        datetime entry_dt
        string extension_name 
        string extension_description
        string extension_version
    }
    StationStatus{
        int station_status_id pk "Internal Key"
        string name "Name of the Station Status"
        datetime lst_updt_ts "Timestamp of the last update"
    }
    URLBlackList {
        int url_blacklist_id pk
        string url_name "Domain name on the blacklist"
        string url_reason "Reason the domain was blacklisted"
        datetime lst_updt_ts "Timestamp of the last update"
    }
```

## Station Stats Data Cube (Star Schema Data Model)
NOTE: Tables will be prefixed with regstats_

```mermaid
erDiagram
    StationStats ||--o{ metrics : metadata
    StationStats ||--|{ StationStatus : metadata
    metricType ||--o{ metrics: assigns
    metricMapping ||--o{ metrics: maps
    metricType {
        int metric_type_id pk
        string name 
        datetime lst_updt_ts
    }
    metrics {
        int metric_id pk
        int metric_type_id fk "linked to MetricType"
        string name "Metric Name"
        string attrib1 "Attribute#1 Optional"
        string attrib2 "Attribute#2 Optional"
        string attrib3 "Attribute#3 Optional"
        string attrib4 "Attribute#4 Optional"
        string attrib5 "Attribute#5 Optional"
        datetime last_updt_ts "Timestamp of the last update"
    }
    metricMapping{
        int metric_mapping_id pk
        int metric_type_id fk
        string source_val "Source value from stations table"
        string target_val "Target Metric Name"
        int metric_id fk "Assigned Metric for this mapping"
        datetime lst_updt_ts
    }
    StationStats {
        int stat_id pk
        date report_dt "Reporting Date required"
        int station_status_id fk
        int metric_id fk
        float data_val
    }
    StationStatus{
        int station_status_id pk "Internal Key"
        string name "Name of the Station Status"
        datetime lst_updt_ts "Timestamp of the last update"
    }

```

## Station Geographical Statistics Data Cube (Star Schema Data Model)
NOTE: Tables will be prefixed with regstats_

```mermaid
erDiagram
    GeoStats ||--o{ Geography : metadata
    GeoStats ||--|{ StationStatus : metadata
    GeographyMapping ||--o{ Geography: maps

    Geography {
        int geo_id pk
        string country_code
        string province
        string city
        datetime last_updt_ts "Timestamp of the last update"
    }
    GeographyMapping{
        int geo_map_id pk
        decimal latitude
        decimal longitude
        string source_country_code
        string source_province
        string source_city
        string target_country_code
        string target_province
        string target_city
        int geo_id fk
        datetime last_updt_ts "Timestamp of the last update"
    }
    GeoStats {
        int geo_stat_id pk
        date report_dt "Reporting Date required"
        int station_status_id fk
        int geo_id fk
        float data_val
    }
    StationStatus{
        int station_status_id pk "Internal Key"
        string name "Name of the Station Status"
        datetime lst_updt_ts "Timestamp of the last update"
    }
```
