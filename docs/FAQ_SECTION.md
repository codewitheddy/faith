# FAQ Section ❓

## Overview
Elegant accordion-style FAQ section that answers common customer questions about ordering, delivery, payments, and more.

## Features

### Design
- **Accordion style**: Click to expand/collapse answers
- **Clean layout**: White background with subtle borders
- **Hover effects**: Pink border on hover
- **Smooth animations**: Expanding/collapsing transitions
- **Icon rotation**: + rotates to × when open

### Questions Covered
1. **How do I place an order?** - Ordering process via WhatsApp
2. **What payment methods do you accept?** - M-Pesa, bank transfer, COD
3. **How long does delivery take?** - 1-2 days Nairobi, 2-4 days Kenya
4. **Do you offer free delivery?** - Free above Ksh 2,000 in Nairobi
5. **Can I return or exchange items?** - 7-day return policy
6. **Are your jewellery pieces authentic?** - Quality assurance
7. **Do you offer gift wrapping?** - Complimentary gift wrapping
8. **How do I care for my jewellery?** - Care instructions

## Implementation

### HTML Structure
```html
<div class="faq-item">
    <div class="faq-question" onclick="toggleFaq(this)">
        <span>Question text</span>
        <span class="faq-icon">+</span>
    </div>
    <div class="faq-answer">
        <p>Answer text</p>
    </div>
</div>
```

### CSS Classes
```css
.faq-section - Section container
.faq-container - Content wrapper (max-width 900px)
.faq-item - Individual FAQ item
.faq-question - Clickable question header
.faq-icon - Plus/minus icon
.faq-answer - Collapsible answer content
.faq-item.active - Expanded state
```

### JavaScript Function
```javascript
function toggleFaq(element) {
    const faqItem = element.parentElement;
    const isActive = faqItem.classList.contains('active');
    
    // Close all items
    document.querySelectorAll('.faq-item').forEach(item => {
        item.classList.remove('active');
    });
    
    // Open clicked item if it wasn't active
    if (!isActive) {
        faqItem.classList.add('active');
    }
}
```

## Behavior

### Accordion Logic
- **Click question**: Opens answer, closes others
- **Click again**: Closes answer
- **Only one open**: Single-item accordion (not multi-select)

### Animations
- **Answer expand**: max-height transition (0 → 500px)
- **Icon rotate**: + rotates 45° to become ×
- **Duration**: 0.3s ease
- **Smooth**: No jarring movements

## User Experience

### Benefits
- ✅ Reduces support inquiries
- ✅ Builds customer confidence
- ✅ Answers common questions
- ✅ Improves conversion rate
- ✅ Professional appearance

### Accessibility
- ✅ Keyboard accessible (clickable)
- ✅ Clear visual feedback
- ✅ Readable text
- ✅ Good contrast

## Navigation Integration

### Added to Menus
- Desktop navigation: "FAQ" link
- Mobile navigation: "FAQ" link
- Smooth scroll to section
- Positioned before Contact section

## Mobile Responsive

### Adjustments
- Smaller heading (2rem vs 2.5rem)
- Reduced padding (20px vs 25-30px)
- Smaller font size (1rem vs 1.1rem)
- Full width on mobile
- Touch-friendly click areas

## Content Strategy

### Question Selection
Questions cover:
- **Ordering process** - How to buy
- **Payment** - Methods accepted
- **Delivery** - Timing and costs
- **Returns** - Policy details
- **Quality** - Authenticity assurance
- **Extras** - Gift wrapping
- **Care** - Maintenance tips

### Answer Style
- Clear and concise
- Friendly tone
- Specific details (timeframes, amounts)
- Action-oriented
- Builds trust

## SEO Benefits

### Keywords
- "How to order jewellery Kenya"
- "Jewellery delivery Nairobi"
- "M-Pesa payment jewellery"
- "Return policy jewellery"
- "Authentic jewellery Kenya"

### Structure
- Proper heading hierarchy
- Question-answer format
- Rich content for indexing
- Internal linking opportunity

## Trust Building

### Transparency
- Clear delivery times
- Upfront about fees
- Return policy stated
- Quality assurance
- Care instructions

### Professionalism
- Well-organized
- Comprehensive coverage
- Proactive communication
- Customer-focused

## Future Enhancements

### Possible Additions
1. Search functionality
2. Category filtering
3. "Was this helpful?" feedback
4. Related questions
5. Video answers
6. Live chat integration
7. More questions based on analytics

## Performance

### Optimization
- Pure CSS animations
- Minimal JavaScript
- No external libraries
- Fast loading
- Smooth interactions

## Design Rationale

### Why Accordion?
- Saves space
- Organized presentation
- Easy to scan
- Common pattern (familiar)
- Mobile-friendly

### Why Single-Select?
- Focuses attention
- Cleaner appearance
- Easier to read
- Less overwhelming
- Better mobile UX

### Why Before Contact?
- Answers questions first
- Reduces contact inquiries
- Logical flow
- Encourages self-service

## Integration

### Works With
- ✅ Navigation menu
- ✅ Smooth scrolling
- ✅ Mobile menu
- ✅ Page layout
- ✅ Brand design

### No Conflicts
- Separate section
- Independent styling
- Own JavaScript
- Clean integration

## Result

A professional, comprehensive FAQ section that builds trust, reduces support inquiries, and improves the overall customer experience! ❓✨

Customers can now find answers to common questions instantly, making them more confident to purchase from The POPSHOP.KE.
