i want to build a web application for my company to create bills & insert customer details, product details

costomers can be added, updated, deleted, and searched & will have following required fields:
- name
- address
- gst number


products can be added, updated, deleted, and searched & will have following required fields:
- name
- hsn code
- unit (kgs or units)

trades are done in kgs & units both & only 2 decimal places are allowed

following are the necessary details of my company:
company name: VIDHIM ENTERPRISES
company address: FIRST FLOOR, 105, BHAURAO UDYOG NAGAR, KHARIGAON , ABOVE S K STEEL, BHAYANDER (E)-401105
company phone: +91 9892352600
company email: vidhimenterprises@gmail.com
GST No: 27AXVPS9856J1Z4

while creating invoice, following things should be considered:
- invoice number should be required & inserted by user
- invoice date should be entered by the user
- client details should be selected from the list of clients
- product details should be selected from the list of products
- quantity should be entered by the user
- rate should be entered by the user


for taxation: only 2 decimal places are allowed 
- cgst should be calculated automatically & rate is 2.5%
- sgst should be calculated automatically & rate is 2.5%
- igst should be calculated automatically & rate is 5%
user can select either cgst & sgst or igst & taxes should be calculated on taxable value


total = taxable value + cgst + sgst + igst + roundoff

taxable value = sum of (quantity * rate) for all products

- roundoff should be calculated automatically means, if taxable value + cgst + sgst + igst is greater than 0.50 then or equal to 0.50 then roundoff should be 1, else 0


also add a button to generate pdf of the bill



a reports page should be there to extract selective or whole information selected by user & filter by date range & extract in pdf format


use flask or django with sqlite database & python