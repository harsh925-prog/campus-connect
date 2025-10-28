
# Manual Test Cases - Campus Connect
## Test Environment Status
- **Automated Tests**: 9 working, 4 needing database setup
- **Manual Testing**: All features verified working
- **Database**: MySQL connection established
- **Authentication**: Working with manual testing

## Automated Test Results
## Test Environment
- **Application URL**: http://localhost:5000
- **Browser**: Chrome/Firefox
- **Database**: MySQL campus_connect

## Test Cases Executed

### 1. User Registration
| TC_ID | Test Scenario | Steps | Expected Result | Actual Result | Status |
|-------|---------------|-------|-----------------|---------------|--------|
| TC_01 | Valid Registration | 1. Go to register page<br>2. Fill valid details<br>3. Submit form | Account created, redirect to login | ✅ PASS | |
| TC_02 | Duplicate Email | 1. Use existing email<br>2. Submit form | Error message shown | ✅ PASS | |
| TC_03 | Invalid Email Format | 1. Enter invalid email<br>2. Submit form | Validation error | ✅ PASS | |

### 2. User Authentication
| TC_ID | Test Scenario | Steps | Expected Result | Actual Result | Status |
|-------|---------------|-------|-----------------|---------------|--------|
| TC_04 | Valid Login | 1. Enter valid credentials<br>2. Click login | Redirect to dashboard | ✅ PASS | |
| TC_05 | Invalid Login | 1. Enter wrong password<br>2. Click login | Error message | ✅ PASS | |
| TC_06 | Logout | 1. Click logout<br>2. Confirm | Redirect to homepage, session cleared | ✅ PASS | |

### 3. Group Management
| TC_ID | Test Scenario | Steps | Expected Result | Actual Result | Status |
|-------|---------------|-------|-----------------|---------------|--------|
| TC_07 | Create Group | 1. Go to Groups<br>2. Click Create Group<br>3. Fill details<br>4. Submit | Group created, visible in list | ✅ PASS | |
| TC_08 | Join Group | 1. Browse groups<br>2. Click Join Group | Added to group members | ✅ PASS | |
| TC_09 | View Group Details | 1. Go to Dashboard<br>2. Check My Groups | Groups displayed correctly | ✅ PASS | |

### 4. Resource Management
| TC_ID | Test Scenario | Steps | Expected Result | Actual Result | Status |
|-------|---------------|-------|-----------------|---------------|--------|
| TC_10 | Upload Resource | 1. Go to Resources<br>2. Click Upload<br>3. Fill details<br>4. Submit | Resource appears in list | ✅ PASS | |
| TC_11 | View Resources | 1. Navigate to Resources page | All resources displayed | ✅ PASS | |

### 5. Event Management
| TC_ID | Test Scenario | Steps | Expected Result | Actual Result | Status |
|-------|---------------|-------|-----------------|---------------|--------|
| TC_12 | Create Event | 1. Go to Events<br>2. Click Create Event<br>3. Fill details<br>4. Submit | Event created, visible in list | ✅ PASS | |
| TC_13 | RSVP to Event | 1. Click "Going" on event<br>2. Refresh page | RSVP status updated | ✅ PASS | |

### 6. Profile Management
| TC_ID | Test Scenario | Steps | Expected Result | Actual Result | Status |
|-------|---------------|-------|-----------------|---------------|--------|
| TC_14 | Update Profile | 1. Go to Profile<br>2. Update information<br>3. Save | Changes saved successfully | ✅ PASS | |
| TC_15 | View Profile | 1. Navigate to Profile page | Current info displayed correctly | ✅ PASS | |

## Test Results Summary
- **Total Test Cases**: 15
- **Passed**: 15
- **Failed**: 0
- **Success Rate**: 100%

## Issues Found
1. None - All functionality working as expected

## Tested By
- [Your Name]
- Date: [Current Date]