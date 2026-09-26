const API_BASE_URL = "http://127.0.0.1:5000";

export async function getTrains() {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/trains`
  );

  if (!response.ok) {
    throw new Error("Failed to fetch trains");
  }

  return response.json();
}

export async function searchTrains(
  source,
  destination
) {
  const params = new URLSearchParams({
    source,
    destination
  });

  const response = await fetch(
    `${API_BASE_URL}/api/v1/search?${params.toString()}`
  );

  if (!response.ok) {
    throw new Error("Failed to search trains");
  }

  return response.json();
}

export async function createBooking(bookingData) {
  const response = await fetch(
    `${API_BASE_URL}/api/v1/bookings`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(bookingData)
    }
  );

  const result = await response.json();

  if (!response.ok) {
    throw new Error(
      result.message || "Failed to create booking"
    );
  }

  return result;
}