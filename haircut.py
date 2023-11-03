import requests
import time
import urllib
import base64

BASE_URL = "https://www.ailabapi.com"
HAIRCUT_API_ENDPOINT = "/api/portrait/effects/hairstyle-editor-pro"
GET_ASYNC_TASK_QUERY_ENDPOINT = "/api/common/query-async-task-result"
API_KEY = "OXqnSbcJaGN0CazUDOrcmNxMZRiyPrpjTb4R3Ii6JoWdBZA7B59LYV5netsQl1lz"
HAIRCUTS = {
    1: "BuzzCut",
    2: "LowFade",
    3: "TexturedFringe",
    4: "Pompadour",
    5: "UnderCut",
    6: "SlickBack",
}


def generate_haircut_ai(*, image, haircut: int):
    headers = {"ailabapi-api-key": API_KEY}
    hairstyle = HAIRCUTS.get(int(haircut))
    data = {
        "task_type": "async",
        "hair_style": hairstyle,
        "reference": "1",
    }
    files = {"image": image}

    try:
        result = requests.post(
            BASE_URL + HAIRCUT_API_ENDPOINT,
            headers=headers,
            files=files,
            data=data,
        )
        if result.status_code != 200:
            return "Failed to generate haircut: " + result.text

        if result.json().get("error_code") != 0:
            return "Failed to generate haircut: " + result.json().get("error_msg")

        task_id = result.json().get("task_id")
        task_result = get_haircut_image_async_task_result(task_id=task_id)

        if isinstance(task_result, str):
            return "Failed to generate haircut: " + task_result

        generated_image = task_result.get("data").get("images")[0]
        if not generated_image:
            return "Failed to generate haircut: " + task_result.get("error_msg")

        # image_path, _ = urllib.request.urlretrieve(generated_image, "haircut-image.jpg")
        # image_to_base64(image_path=image_path)
        return generated_image

    except Exception as e:
        print(e)
        return "Failed to generate haircut: " + str(e)


def get_haircut_image_async_task_result(*, task_id: str):
    headers = {"ailabapi-api-key": API_KEY}
    max_retries = 20  # Define the maximum number of retries
    retry_interval = 1  # Retry every 2 seconds

    for retry in range(max_retries):
        try:
            time.sleep(2)

            result = requests.get(
                BASE_URL + GET_ASYNC_TASK_QUERY_ENDPOINT,
                headers=headers,
                params={"task_id": task_id},
            )

            if result.status_code != 200:
                return "Failed to haircut result image: " + result.text

            task_status = result.json().get("task_status")

            if task_status == 2:
                return result.json()
            else:
                if retry < max_retries - 1:
                    # Task is still running, retry after the specified interval
                    print(
                        "Task is still running, retrying in "
                        + str(retry_interval)
                        + " seconds"
                    )
                    time.sleep(retry_interval)
                    continue

            # If task_status is not 1 or 2, or max retries are exhausted, return an error message
            return "Failed to get generate haircut: Task status is not 1 or 2"

        except Exception as e:
            print(e)
            if retry < max_retries - 1:
                # Retry if an exception occurred and we haven't exhausted retries
                time.sleep(retry_interval)
                continue
            return "Failed to get generate haircut: " + str(e)

    return "Failed to get generate haircut: Maximum retries reached"


def image_to_base64(*, image_path: str):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
        return encoded_string
