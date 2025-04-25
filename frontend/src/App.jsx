import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Home from './pages/Home/Home';
import Login from './pages/auth/Login';
import PrivateRoute from './components/PrivateRoute';
// import Register from './pages/auth/Register';
import ForgotPassword from './pages/auth/ForgotPassword';
import ResetPassword from './pages/auth/ResetPassword';
import Dashboard from './pages/Dashboard/Dashboard';
import Profile from './pages/Dashboard/Profile';
import TrackChallenges from './pages/TrackChallenges/TrackChallenges';
import ChallengeDetail from './pages/ChallengeDetail/ChallengeDetail';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        {/* <Route path="/register" element={<Register />} /> */}
        <Route path="/forgot-password" element={<ForgotPassword />} />
        <Route path="/reset-password/:uid/:token/" element={<ResetPassword />} />
        
        <Route element={<PrivateRoute />}>
          <Route path="/dashboard" element={<Dashboard />} />
        </Route>

        <Route path='/profile' element={<Profile />} />
        <Route path="/tracks/:trackId/challenges" element={<TrackChallenges />} />
        <Route path="/challenges/:challengeId" element={<ChallengeDetail />} />
      </Routes>
    </Router>
  );
}

export default App;