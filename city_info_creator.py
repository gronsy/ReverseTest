import requests


def get_city_temperature(weather_response_json, city_name):
    temperature = weather_response_json['main']['temp']

    return "Current temperature in " + str(city_name) + " is " + str(temperature) + " degrees Celsius."


def create_output_file(weather_response_json, summary_response_json, city_name):
    city_temperature_output = get_city_temperature(weather_response_json, city_name)
    file_name = city_name + ".txt"

    # re-writing old data from a file assuming that it would be refreshing the old data
    with open(file_name, "w") as output_file:
        output_file.write(summary_response_json['extract'] + "\n" + city_temperature_output)

    output_file.close()


def create_request(url, request_type):
    api_response = requests.get(url)

    if api_response.status_code == 404:
        throw_error(api_response.json(), request_type)

    return api_response


def throw_error(api_response_json, request_type):
    error_message_base = "Failed to make request with code 404: "
    if request_type == "weather":
        raise NameError(error_message_base + api_response_json['message'])
    elif request_type == "summary":
        raise NameError(error_message_base + api_response_json['detail'])


def make_api_calls(city_name):
    try:
        # added metric so i don't need to convert kelvin to celsius programmatically
        weather_url = "http://api.openweathermap.org/data/2.5/weather?q=" + city_name + \
                      "&APPID=15bf51e94a29c728f34f933992b31cb2&units=metric"
        summary_url = "https://en.wikipedia.org/api/rest_v1/page/summary/" + city_name

        weather_response = create_request(weather_url, "weather")
        summary_response = create_request(summary_url, "summary")

        create_output_file(weather_response.json(), summary_response.json(), city_name)
    except NameError as e:
        print("Error while querying city: " + city_name + "\nError: " + str(e))
    except ValueError:
        print("Incorrect value specified for request type.")


if __name__ == '__main__':
    print("If you want to exit program input quit!")

    while True:
        city_name_input = input("Please input the name of the city: ")
        if city_name_input.lower() == "quit":
            break
        elif city_name_input.strip(" ") == "":
            print("Please specify city name.")

        make_api_calls(city_name_input)
