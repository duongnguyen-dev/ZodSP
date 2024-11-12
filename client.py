import requests
import cv2

if __name__ == "__main__":
    url = 'http://zod.com/detect/'
    headers = {
        'Content-Type': 'application/json',
        # Add other headers if required (e.g., 'Authorization': 'Bearer YOUR_TOKEN')
    }

    data = {"prompt": "car"}
    file = {"data" : open("assets/test_2.jpeg", "rb")}
        
    response = requests.post(url, params=data, files=file)

    if response.status_code == 200:
        print("Success:", response.json())
        image = cv2.imread("assets/test_2.jpeg", cv2.IMREAD_COLOR)
        # Example response data with bounding boxes
        response_data = response.json()
        
        # Draw bounding boxes on the image
        for item in response_data:
            x1, y1, x2, y2, label, score = item['response_data']
            color = (0, 255, 0)  # Green for the bounding box
            thickness = 2
            cv2.rectangle(image, (x1, y1), (x2, y2), color, thickness)
            cv2.putText(image, f'{label}: {score:.2f}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        cv2.imshow("result", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        print("Error:", response.status_code, response.text)
