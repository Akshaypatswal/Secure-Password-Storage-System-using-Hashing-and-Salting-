# Testing Guide

## Accessibility (A11Y) Checklist

### WCAG 2.1 AA Compliance

#### Perceivable
- [ ] All images have alt text
- [ ] Text has sufficient color contrast (4.5:1 for normal text, 3:1 for large text)
- [ ] Content is readable without color alone
- [ ] Text can be resized up to 200% without loss of functionality
- [ ] Audio/video has captions or transcripts

#### Operable
- [ ] All functionality is keyboard accessible
- [ ] No keyboard traps
- [ ] Focus indicators are visible
- [ ] Sufficient time limits (or can be extended)
- [ ] No content that causes seizures
- [ ] Clear navigation and headings

#### Understandable
- [ ] Language is clear and simple
- [ ] Form labels and instructions are clear
- [ ] Error messages are descriptive
- [ ] Consistent navigation and functionality

#### Robust
- [ ] Valid HTML/CSS
- [ ] Screen reader compatible
- [ ] Works with assistive technologies

### Browser Testing
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile browsers (iOS Safari, Chrome Android)

### Screen Reader Testing
- [ ] NVDA (Windows)
- [ ] JAWS (Windows)
- [ ] VoiceOver (macOS/iOS)
- [ ] TalkBack (Android)

## Camera Scan Test Cases

### Test Case 1: Consent Flow
**Steps:**
1. Navigate to onboarding page
2. Click "Start with Camera Scan"
3. Verify consent modal appears
4. Read all sections
5. Click "I Understand, Proceed"

**Expected:**
- Consent modal displays all required information
- All sections are readable
- Accept button enables after reading
- Camera scan starts after acceptance

### Test Case 2: Camera Access Denied
**Steps:**
1. Deny camera permission in browser
2. Attempt to start camera scan

**Expected:**
- Error message displayed
- Fallback to manual selection
- User can proceed without camera

### Test Case 3: Sign Language Detection
**Steps:**
1. Accept consent
2. Start camera scan
3. Wave hands / make signing gestures for 20 seconds
4. Complete scan

**Expected:**
- System detects hand movements
- Recommendation suggests "Sign Language Interface"
- Confidence score > 0.7
- Explainability cues mention hand gestures

### Test Case 4: Voice Detection
**Steps:**
1. Accept consent
2. Start camera scan
3. Speak clearly during scan
4. Complete scan

**Expected:**
- System detects speech
- Recommendation suggests "Voice-First Interface"
- Confidence score > 0.7
- Explainability cues mention speech detection

### Test Case 5: Low Confidence
**Steps:**
1. Accept consent
2. Start camera scan
3. Remain still / minimal interaction
4. Complete scan

**Expected:**
- Recommendation has confidence < 0.7
- System suggests manual selection
- User can override recommendation

### Test Case 6: Manual Override
**Steps:**
1. Complete camera scan
2. Receive recommendation
3. Click "Choose Different Mode"
4. Select different mode manually

**Expected:**
- Manual selection form appears
- User can select any mode
- Selection is saved correctly

### Test Case 7: Skip Camera
**Steps:**
1. Navigate to onboarding
2. Click "Skip Camera - Manual Selection"
3. Select assist mode manually

**Expected:**
- Camera scan is skipped
- Manual selection form appears
- User can complete onboarding without camera

### Test Case 8: Data Deletion
**Steps:**
1. Complete onboarding with camera scan
2. Navigate to settings
3. Click "Delete All Data"
4. Confirm deletion

**Expected:**
- All user data is deleted
- User is redirected to onboarding
- No data remains in storage

## Interface Mode Test Cases

### Voice Interface
- [ ] Voice commands work
- [ ] Screen reader compatible
- [ ] Audio feedback provided
- [ ] Text-to-speech functional

### Sign Interface
- [ ] Sign language avatar displays
- [ ] Text chat functional
- [ ] Quick reply buttons work
- [ ] Large text readable

### Text Interface
- [ ] Large text displays correctly
- [ ] Visual indicators clear
- [ ] Text input functional
- [ ] Text-to-speech optional

### Gesture Interface
- [ ] Gesture detection works
- [ ] Touch controls functional
- [ ] Adaptive UI responds
- [ ] Feedback provided

### Motor Interface
- [ ] Large buttons accessible
- [ ] Switch mode functional
- [ ] Simplified navigation works
- [ ] High contrast mode available

## API Test Cases

### Test Case: POST /api/assist-scan
**Request:**
```json
{
  "features": {
    "handSignFreq": 6.5,
    "speechDetected": false,
    "gazePattern": "normal",
    "posture": "seated",
    "interactionBehavior": null
  },
  "duration": 20
}
```

**Expected Response:**
```json
{
  "mode": "sign",
  "confidence": 0.92,
  "cues": [
    "Detected repeated hand-signing gestures (frequency: 6.5)",
    "Strong indication of sign language preference"
  ],
  "scores": {
    "voice": 0.1,
    "sign": 0.92,
    "text": 0.2,
    "gesture": 0.3,
    "motor": 0.2
  },
  "explainability": {
    "top_features": [["sign", 0.92], ["gesture", 0.3], ["text", 0.2]],
    "reasoning": "Strong recommendation for sign mode based on clear interaction patterns."
  }
}
```

### Test Case: POST /api/preferences
**Request:**
```json
{
  "user_id": "user123",
  "assist_mode": "sign",
  "source": "camera_recommendation",
  "confidence": 0.92,
  "completed_onboarding": true
}
```

**Expected Response:**
```json
{
  "user_id": "user123",
  "assist_mode": "sign",
  "source": "camera_recommendation",
  "confidence": 0.92,
  "preferences": null,
  "completed_onboarding": true,
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

### Test Case: GET /api/assist-preview?mode=sign
**Expected Response:**
```json
{
  "mode": "sign",
  "name": "Sign Language Interface",
  "description": "Optimized for deaf and hard-of-hearing users",
  "features": ["Sign language avatar", "Text chat", "Visual alerts"],
  "demo_url": "/demo/sign"
}
```

## Performance Testing

### Load Testing
- [ ] API handles 100 concurrent requests
- [ ] Frontend loads in < 3 seconds
- [ ] Camera scan completes in 20 seconds
- [ ] Recommendation generated in < 1 second

### Browser Performance
- [ ] No memory leaks
- [ ] Smooth animations (60fps)
- [ ] Responsive on mobile devices
- [ ] Works offline (basic features)

## Security Testing

- [ ] No sensitive data in client-side code
- [ ] API endpoints require authentication (production)
- [ ] Data encryption in transit and at rest
- [ ] XSS protection
- [ ] CSRF protection
- [ ] SQL injection prevention

## Privacy Testing

- [ ] Consent modal appears on first use
- [ ] Camera data not stored without consent
- [ ] Data deletion works correctly
- [ ] No data sent to third parties without consent
- [ ] Local storage encryption works

## Manual Test Script

1. **Setup:**
   - Install dependencies
   - Start backend server
   - Start frontend dev server

2. **Onboarding Flow:**
   - Test consent modal
   - Test camera scan
   - Test recommendation display
   - Test manual selection

3. **Interface Testing:**
   - Test each assist mode
   - Verify functionality
   - Check accessibility

4. **Settings:**
   - Test mode switching
   - Test data deletion
   - Verify preferences saved

5. **API Testing:**
   - Test all endpoints
   - Verify responses
   - Check error handling

---

**Note:** For production deployment, conduct comprehensive user testing with actual disabled users and accessibility experts.

