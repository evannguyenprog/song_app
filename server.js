const express = require('express');
const session = require('express-session');
const passport = require('passport');
const SpotifyStrategy = require('passport-spotify').Strategy;

const app = express();
const PORT = process.env.PORT || 3001;

app.use(session({ secret: 'your-secret-key', resave: true, saveUninitialized: true }));
app.use(passport.initialize());
app.use(passport.session());

// Passport configuration
passport.use(new SpotifyStrategy({
  clientID: 'your-client-id',
  clientSecret: 'your-client-secret',
  callbackURL: 'http://localhost:3001/auth/spotify/callback',
},
function(accessToken, refreshToken, expires_in, profile, done) {
  // Save user data in the database
  // For simplicity, you can use an in-memory array or connect to your PostgreSQL database
  return done(null, profile);
}));

passport.serializeUser((user, done) => {
  done(null, user);
});

passport.deserializeUser((obj, done) => {
  done(null, obj);
});

// Define your routes here

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});

// ...

app.get('/auth/spotify', passport.authenticate('spotify', { scope: ['user-read-email', 'user-read-private'] }));

app.get('/auth/spotify/callback',
  passport.authenticate('spotify', { failureRedirect: '/' }),
  (req, res) => {
    // Successful authentication, redirect to the React app
    res.redirect('http://localhost:3000');
  });

app.get('/logout', (req, res) => {
  req.logout();
  res.redirect('/');
});

// Example protected route
app.get('/profile',
  require('connect-ensure-login').ensureLoggedIn(),
  (req, res) => {
    res.json(req.user);
  });

// ...
