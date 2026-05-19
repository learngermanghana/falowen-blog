import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import A1Day25TagesablaufWorkbook from './components/A1Day25TagesablaufWorkbook';

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/campus/course/day-25-tagesablauf-workbook" element={<A1Day25TagesablaufWorkbook />} />
      </Routes>
    </Router>
  );
};

export default App;
