FORMAT: 1A
HOST:http://dev.jayveehe_staticinfo.avosapps.com/

# Senz.analyzer.user.staticinfo.degree

User's static info predictor,degree included.
You can view the code at Github [Senz.analyzer.user.staticinfo.degree](https://github.com/petchat/senz.analyzer.user.staticinfo.degree)

## Group API

## static info data [/static_info/data{?limit}{?label}]
The result of static_info/data has 3 attributes:

+ app - Name of the app, String.
+ degree - Weight of the label, Float.
+ label - Label of the app, String.
+ Parameters

    + limit: 100 (optional,number) - Limit number of the result.
    + label: gender (optional,string) - Expected Label of the result.
    
### Get remote appslist data [GET]

+ Response 200 (application/json)
        
            [
                {
                    "app": "app_name_1",
                    "degree": app_degree_1,
                    "label": "pp_label_1"
                },
                {
                    "app": "app_name_n",
                    "degree": app_degree_n,
                    "label": "app_label_n"
                }
            ]
            


## static info predict [/static_info/predict]
The result of static info predict has following attributes:

+ {label} - The key shows a label, and the value is the probability of this label.

### Predict the labels by user's app_list. [POST]
+ Request (application/json)

        {
            "app_list": ["com.yidian.nba","com.dota.emu"]
        }

+ Response 200 (application/json)

        {
            "gender": 0.193666930476603
        }
