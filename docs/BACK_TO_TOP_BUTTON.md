# Back to Top Button ↑

## Overview
Smooth, elegant back-to-top button that appears when scrolling down the page.

## Features

### Design
- **Shape**: Circular button (50px diameter)
- **Color**: Pastel pink background (#F8C8DC)
- **Icon**: Upward arrow (↑)
- **Position**: Fixed, bottom-right corner
- **Shadow**: Soft pink shadow for depth

### Behavior
- **Hidden by default**: Only appears after scrolling 300px down
- **Smooth fade-in**: Elegant opacity transition
- **Smooth scroll**: Animated scroll to top (not instant jump)
- **Hover effect**: Lifts up with darker pink color
- **Active state**: Slight press effect

### Positioning
- **Desktop**: 
  - Bottom: 100px (above cart icon)
  - Right: 30px
  - Size: 50px × 50px

- **Mobile**:
  - Bottom: 80px (above cart icon)
  - Right: 20px
  - Size: 45px × 45px

## Implementation

### CSS Classes
```css
.back-to-top - Base button styling
.back-to-top.visible - Shows button (opacity 1)
```

### JavaScript Functions
```javascript
// Show/hide based on scroll position
window.addEventListener('scroll', function() {
    if (window.scrollY > 300) {
        backToTop.classList.add('visible');
    } else {
        backToTop.classList.remove('visible');
    }
});

// Smooth scroll to top
function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}
```

## User Experience

### Visibility Trigger
- Appears after scrolling **300px** down
- Ensures user has scrolled enough to need it
- Doesn't clutter the initial view

### Smooth Animation
- **Fade in**: 0.3s transition
- **Scroll**: Smooth behavior (not instant)
- **Hover**: Lifts 5px with shadow increase
- **Click**: Slight press effect

### Positioning Logic
- Above cart icon (doesn't overlap)
- Right side (consistent with cart)
- Fixed position (always accessible)
- High z-index (999, below modals)

## Accessibility

### Current
- ✅ Button element (keyboard accessible)
- ✅ Title attribute ("Back to top")
- ✅ Clear visual indicator (arrow)
- ✅ Good color contrast

### Future Enhancements
- Add aria-label
- Add keyboard shortcut (Home key)
- Add focus indicator

## Mobile Responsive

### Adjustments
- Smaller size (45px vs 50px)
- Adjusted position (80px vs 100px from bottom)
- Same functionality
- Touch-friendly size

## Browser Compatibility

### Supported
- ✅ Chrome/Edge (smooth scroll)
- ✅ Firefox (smooth scroll)
- ✅ Safari (smooth scroll)
- ✅ Mobile browsers

### Fallback
- Browsers without smooth scroll support will jump instantly
- Still functional, just less elegant

## Performance

### Optimized
- CSS transitions (GPU accelerated)
- Scroll listener (passive)
- No layout thrashing
- Minimal JavaScript

## Design Rationale

### Color Choice
- Pastel pink matches brand
- Stands out but not jarring
- Consistent with other UI elements

### Position
- Right side (standard convention)
- Above cart icon (logical stacking)
- Fixed (always accessible)

### Size
- 50px (easy to click)
- 45px mobile (touch-friendly)
- Circular (friendly, approachable)

## Integration

### Works With
- ✅ Cart icon (positioned above)
- ✅ Toast notifications (different z-index)
- ✅ Modals (lower z-index)
- ✅ Navbar scroll effects

### No Conflicts
- Separate z-index layer
- Independent positioning
- Own event handlers

## Benefits

### User Experience
- ✅ Quick navigation to top
- ✅ Saves scrolling effort
- ✅ Professional appearance
- ✅ Smooth, elegant motion

### Accessibility
- ✅ Keyboard accessible
- ✅ Clear purpose
- ✅ Always available when needed

### Design
- ✅ Matches brand aesthetic
- ✅ Minimal, unobtrusive
- ✅ Smooth animations
- ✅ Mobile responsive

## Usage Statistics

### When It Appears
- After scrolling 300px (approximately past hero section)
- Remains visible until scrolling back to top 300px

### Typical Use Cases
- After browsing products
- After reading about section
- After viewing contact info
- Quick return to navigation

## Result

A polished, professional back-to-top button that enhances navigation and user experience! ↑✨
