import {
  BrowserRouter,
  Routes,
  Route
} from "react-router-dom";

import Home from "./pages/Home";
import SearchResults from "./pages/SearchResults";
import PassengerDetails from "./pages/PassengerDetails";
import BookingSummary from "./pages/BookingSummary";
import BookingConfirmation from "./pages/BookingConfirmation";
import NotFound from "./pages/NotFound";

function App() {
  return (
    <BrowserRouter>
      <Routes>

        <Route
          path="/"
          element={<Home />}
        />

        <Route
          path="/search-results"
          element={<SearchResults />}
        />

        <Route
          path="/passenger-details"
          element={<PassengerDetails />}
        />

        <Route
          path="/booking-summary"
          element={<BookingSummary />}
        />

        <Route
          path="/booking-confirmation"
          element={<BookingConfirmation />}
        />

        <Route
          path="*"
          element={<NotFound />}
        />

      </Routes>
    </BrowserRouter>
  );
}

export default App;