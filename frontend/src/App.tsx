import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import HomePage from './components/HomePage';
import ListingsPage from './components/ListingsPage';

const App: React.FC = () => {
    return (
        <Router>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/listings" element={<ListingsPage />} />
            </Routes>
        </Router>
    );
};

export default App;