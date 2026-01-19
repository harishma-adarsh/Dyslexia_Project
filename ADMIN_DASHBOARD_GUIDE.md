# Admin Dashboard Documentation

## Overview
The admin dashboard provides comprehensive management and monitoring capabilities for the Dyslexia Detection System.

## Access

### Admin Login
- **URL**: `http://localhost:8000/admin-login/`
- **Default Credentials**:
  - Username: `admin`
  - Password: `admin123`

### Creating Additional Admin Users
To create additional admin users, use Django's management command:
```bash
python manage.py createsuperuser
```

Or use the custom setup command:
```bash
python manage.py setup_admin
```

## Features

### 1. Dashboard (`/admin-dashboard/`)
The main dashboard provides a comprehensive overview of the system:

#### User Statistics
- **Total Users**: Count of all registered students
- **Active Users (30 Days)**: Users who logged in within the last 30 days
- **New Users (7 Days)**: Recent registrations
- **Total Detections**: All detection analyses performed

#### Sample Statistics
- **Handwriting Samples**: Total uploaded handwriting samples
- **Speech Samples**: Total uploaded audio recordings
- **Video Samples**: Total uploaded video files
- **Samples Today**: New uploads today

#### Detection Analytics
- **Risk Level Distribution**: Visual breakdown of high/medium/low risk detections
- **Average Probabilities**: Mean dyslexia and dysgraphia detection probabilities
- **Detection Confidence**: System confidence in detection results

#### Training Statistics
- **Active Exercises**: Number of available training games
- **Total Sessions**: All completed exercise sessions
- **Average Score**: Mean performance across all sessions
- **Users with Progress**: Students actively using training exercises
- **Average Mastery**: Overall mastery level across all users

#### Recent Activity
- **Recent Detections**: Latest 10 detection results with risk levels
- **Recent Users**: Newest 10 registered users
- **Recent Sessions**: Latest training exercise completions
- **Top Performers**: Users with highest average scores

### 2. User Management (`/admin-users/`)
View and manage all registered users:

**Information Displayed:**
- Username
- Age and Grade Level
- Registration Date
- Last Login
- Number of Detections
- Number of Training Sessions
- Latest Risk Level

**Use Cases:**
- Monitor user engagement
- Identify users who need attention
- Track user progress over time
- Analyze user demographics

### 3. Detection Management (`/admin-detections/`)
View all detection results with filtering capabilities:

**Information Displayed:**
- User who performed the detection
- Detection timestamp
- Risk level (High/Medium/Low)
- Dyslexia probability
- Dysgraphia probability
- Overall risk score
- Detection confidence
- Sample types used (Handwriting/Speech)

**Features:**
- Filter by risk level
- Sort by date
- View detailed detection metrics

**Use Cases:**
- Monitor detection accuracy
- Identify trends in detection results
- Track high-risk cases
- Analyze system performance

### 4. Exercise Management (`/admin-exercises/`)
Manage and monitor training exercises:

**Information Displayed:**
- Exercise name and description
- Exercise type (Reading/Writing/Phoneme)
- Difficulty level (Beginner/Intermediate/Advanced)
- Active/Inactive status
- Number of sessions completed
- Average score
- Number of unique users
- Expected duration

**Use Cases:**
- Monitor exercise popularity
- Identify effective exercises
- Track user engagement with different exercise types
- Optimize exercise offerings

## Security

### Authentication
- Admin access requires staff or superuser privileges
- Separate login system from student accounts
- Session-based authentication
- Secure password hashing

### Authorization
All admin views are protected with:
```python
@login_required
@user_passes_test(is_admin, login_url='admin_login')
```

### Best Practices
1. **Change Default Password**: Immediately change the default admin password in production
2. **Use Strong Passwords**: Require complex passwords for admin accounts
3. **Limit Admin Access**: Only grant admin privileges to trusted personnel
4. **Monitor Admin Activity**: Regularly review admin actions
5. **Enable HTTPS**: Use SSL/TLS in production environments

## Navigation

The admin interface includes a consistent navigation bar with:
- Dashboard (Overview)
- Users (User Management)
- Detections (Detection Results)
- Exercises (Exercise Management)
- Logout

## Design Features

### Visual Design
- Modern gradient-based color scheme (Purple to Blue)
- Responsive layout for mobile and desktop
- Card-based statistics display
- Interactive hover effects
- Clean, professional typography

### User Experience
- Intuitive navigation
- Clear data visualization
- Quick access to key metrics
- Responsive tables
- Color-coded badges for status indicators

### Color Coding
- **High Risk**: Red badges
- **Medium Risk**: Orange badges
- **Low Risk**: Green badges
- **Active Status**: Blue badges
- **Reading Exercises**: Blue
- **Writing Exercises**: Green
- **Phoneme Exercises**: Orange

## API Integration

The admin dashboard pulls data from:
- `User` model (Django auth)
- `UserProfile` model (data_collection)
- `HandwritingSample`, `SpeechSample`, `VideoSample` (data_collection)
- `DetectionResult` (detection_module)
- `Exercise`, `UserProgress`, `ExerciseSession` (training_module)

## Performance Considerations

### Optimizations
- Database query optimization with `select_related()` and `prefetch_related()`
- Aggregation queries for statistics
- Efficient filtering and sorting
- Pagination for large datasets (can be added)

### Scalability
For large deployments, consider:
- Adding pagination to tables
- Implementing caching for statistics
- Using database indexes
- Implementing background tasks for heavy computations

## Troubleshooting

### Cannot Login
1. Verify admin user exists: `python manage.py setup_admin`
2. Check user has staff/superuser privileges
3. Ensure correct URL: `/admin-login/` (not `/admin/`)

### Missing Data
1. Verify database migrations are applied
2. Check that models are properly registered
3. Ensure data collection is working

### Permission Denied
1. Verify user has `is_staff=True` or `is_superuser=True`
2. Check authentication middleware is enabled
3. Verify session is valid

## Future Enhancements

Potential improvements:
1. **Export Functionality**: Export data to CSV/Excel
2. **Advanced Filtering**: More filter options for all views
3. **Charts and Graphs**: Visual analytics with Chart.js or similar
4. **Email Notifications**: Alert admins of high-risk detections
5. **Audit Logging**: Track admin actions
6. **Bulk Operations**: Manage multiple users/exercises at once
7. **Search Functionality**: Search users, detections, exercises
8. **Date Range Filters**: Filter by custom date ranges
9. **User Detail Pages**: Detailed view of individual users
10. **Exercise Editor**: Create/edit exercises through UI

## Support

For issues or questions:
1. Check this documentation
2. Review Django logs
3. Verify database integrity
4. Check browser console for JavaScript errors
