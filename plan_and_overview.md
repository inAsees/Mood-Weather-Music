**Mood-Based Song Recommendation App - Plan & Overview**

## **Project Overview**

This application takes user input for their **mood** and **city**, checks the current weather conditions using OpenWeatherMap, and determines if the weather matches the user’s mood. Based on the mood, it fetches a song recommendation from Last.fm. The backend is implemented using **FastAPI**.

---

## **Key Features**

- **User Input:** Accepts **mood** and **city**.
- **Weather Fetching:** Retrieves real-time weather data from OpenWeatherMap.
- **Mood-Weather Matching:** Determines if the mood aligns with the weather.
- **Song Recommendation:** Fetches a song from Last.fm based on mood.
- **FastAPI-Based API:** RESTful API endpoints for smooth interaction.
- **Postman Collection:** Includes pre-configured requests for testing.
- **Error Handling & Unit Testing:** Ensures stability and reliability.

---

## **Technology Stack**

- **Programming Language:** Python 3.12
- **Backend Framework:** FastAPI
- **APIs Used:** OpenWeatherMap (weather data), Last.fm (song recommendations)
- **HTTP Client:** httpx
- **Data Validation:** Pydantic
- **Testing:** Pytest
- **Documentation:** Postman Collection, README.md

---

## **Workflow**

1. **User Inputs Mood & City**
2. **Fetch Weather Data** → OpenWeatherMap API
3. **Check Mood-Weather Match**
4. **Fetch Song Recommendation** → Last.fm API
5. **Return Recommended Song**

---

## **Error Handling**

- **Invalid City Input:** Returns a user-friendly error message.
- **Unhandled Exceptions:** Logs errors and returns a meaningful response.
