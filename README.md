
# django-petstore

[![Build Status](https://travis-ci.org/jyoung90ie/django-petstore.svg?branch=master)](https://travis-ci.org/jyoung90ie/django-petstore)
[![codecov](https://codecov.io/gh/jyoung90ie/django-petstore/branch/master/graph/badge.svg)](https://codecov.io/gh/jyoung90ie/django-petstore)

This is an E-Commerce store developed using Django.

## UX

### Wireframes

Prior to development of the application, I developed a number of wireframes which demonstrate my vision for how the website should look on multiple devices. You can view these wireframes [here](wireframes/).

### User Stories

## Features

### Existing Features

This package enables you to build and deploy a functional e-commerce website, with payment processing through the secure third-party service, [Stripe](https://stripe.com/).

The package has been broken into individual apps, the features of which are detailed below:

#### Custom User Model

To capture additional user information, such as address, I opted to overrid
the default Django user model and create a custom one. This enabled me to store
all the necessary user data in one object. It will also make any future user
model changes easier to make.

Given the additional data input requirements, I had to specify custom forms in
order to capture all the required information. This included overriding Django
default forms, for example, the admin forms for adding/modifying user details.

#### Accounts

This is where all customer information is retained via the custom user model. I also made the decision
to use Django-allauth which added the ability to override the username field, using the email address
as the login. It also brought with it the ability to verify email addresses and reset passwords.

Within this app I have overriden a number of the default forms provided by allauth to integrate with the customer user model. To produce responsive forms I have used the django-crispy-forms helper function which allows me to create custom form layouts with individual element styling. I have also modified the rendering of the django admin site for the user object, to provide a better structure.

Outlined below are the views that are produced by this app:

a) **Signup:** a custom form used to create a new user account with the custom user model. The username field is removed, with the email address used in it's placed. Given this is an ecommerce application, it made more sense to proceed with email only, as a username would not serve any other function than to login.

b) **Login:** Enables users to login using their email address and password. If any products exist in a user's basket before they login, these will be merged into any existing basket when the user logs in.

c) **Logout:** Enables users to logout of their account. The user will be asked to confirm they wish to logout of their account, this prevents accidental logout. When a user logs out any items added to their basket will no longer be visible, however, the basket will be stored in the account and visible upon login.

d) **Profile - Personal Details:** The user can update their billing address from here. I made the decision to *only* allow billing address to be changed here for security, so that a user can only use payment cards for one billing address. The billing address is passed through to Stripe upon payment processing. When updating details the user will be provided with feedback flash messages to give a more interaction experience and confirm to the user if an update took place or not.

e) **Profile - Change email:** A user can have multiple emails if they wish, this functionality is leveraged from django-allauth. The user can log in with all email addresses under their account. I decided to include this functionality to enable users to have one householder account if they wish.

f) **Profile - Change password:** For security, a user must provide their current password alongside a new password before it will be accepted and updated.

g) **Reset password:** TBC - Functionality provided by django-allauth with a custom template.

#### Basket

The Basket app is made up of two models, Basket and BasketItem. The Basket model is used as a container and linked to a user account. BasketItems are then linked to the Basket, via a Many-to-One relationship (i.e. one basket can have many items). The BasketItems record what products a user has added to their basket and the quantity of each (up to a maximum of 5 for each product).

Given this is an ecommerce application, the basket is a critical component of the application's functionality. It enables anonymous users to create a basket of items, this will be automatically linked to their account/merged with an existing basket upon account login. Users can access their basket at any time to add/update/remove items.

When a basket contains at least one item, the basket icon will display the total item count, to enable the user to keep track of contents without having to click into the basket.

There are a number of components to the basket app, which I have outlined below:

a) **Add to Basket:** This view is used to add items to the Basket object. If a Basket object does not yet exist it will be created and the product added as a related BasketItem object. Products are automatically added with a quantity of 1, which can be updated in the basket view.

This view will only accept valid product IDs. To prevent accidentally adding the wrong products, the product object ID has been changed to use a UUID.

Feedback flash messages are provided to the user when a product is successfully added, and when adding an item will result in it exceeding the maximum permitted single-item quantity.

b) **View/Update Basket:** This template makes use of the Django inline formset factory functionality, this enables the updating of multiple database objects at once through a single form. I have setup the form to permit the user to change product quantity and/or remove a product.

Feedback messages are provided to inform the user whether the basket update was successful or not.

c) **Middleware:** I have created a custom BasketMiddleware class which checks to see if the user has a session variable, basket_id, which is created when a new Basket object is created (step a). I use this to pass-through the user's Basket object as part of Django's Request object. I decided to use this method instead of creating multiple session variables because it maintains a single source of truth (the database), and enables me to access the Basket model and associated methods on any view, for example, rendering item count above the basket icon.

d) **Basket/BasketItem model methods:** Within the Basket model I have created a number of helper functions which enable me to easily check/display values, e.g. item subtotals, total item count, and basket total.

e) **Linking a Basket to an account:** Through the use of the Django signal, user_logged_in, I have created a function (get_basket) which determines if the user logging in to their account has a basket already stored in the database, if they do this is merged with any items added to their basket prior to login. If no basket existed previously, the basket is then linked to the specific user account and will always be available upon login.

f) **Customised Admin Functionality:** Given the relationship between Basket and BasketItem, I have amended the admin view so that when accessing a basket, the contents (basketitems) will be displayed with it. The contents can be modified.

g) **Create Order:** The Basket model also contains a helper method which is used to 'convert' a basket into an order. This is only called once payment has been verified. This will be discussed further under the *Checkout* app.

#### Checkout

The Checkout app is used to process an order and can only be accessed when a user is logged in with at least one item in their basket. This process captures the user's billing address (from user object) and shipping address (pre-populated from user object address) which is modifiable. Prior to processing payment, the user is asked to review and confirm their order, with payment processing handled by a third-party payment processing service, Stripe.

The models for this app have a similiar structure to that of the Basket app, Checkout and CheckoutItem, the difference in this instance, is that more information is captured. An important distinction is the additional of an Order status field AND an OrderItem status field, enabling site admins and users to clear understand the status of relevant orders. Prices are also saved, as user's are charged at a point-in-time, whereas, product pricing may fluctuate overtime.

The BasketItem object is converted to CheckoutItem, with each CheckoutItem representing a single-item (quantity=1), so if a BasketItem has a quantity of 5, this will result in the creation of 5 CheckoutItems. This enables me to individually handle each item of a user's order, i.e. I can provide status against each item, for example, the stock for a product = 2, but the user ordered 3. I can ship those which I have, updating them to reflect this, and ship the third item when it becomes available.

This app is made-up of the following key components:

a) **Process Order:** This is a view that combines two forms, user shipping and billing details, and the Stripe payment form. The forms are customised using django-crispy-forms with custom kwargs passed-through.

The structure of the form has been designed to capture the required user details, before displaying a summarised version of the user's order, with the payment form only being displayed once the user has confirmed their order.

The payment form is handled using Stripe v3 with a combination of JavaScript (JS) and server-side rendering. Once the payment has been made, a custom JS function adds a hidden field to the form, before posting the form. With the POST request, the serverside verifies the token using Stripe's PaymentIntent API. If there were any user related issues, for example, declined card, this will be fedback to the user.

Once the payment is verified through Stripe the Basket model *create_order method* is called - see below for further detail.

d) **Basket create_order() method:** This creates an Order object, using the information captured from the billing/shipping details form and the user's Basket Object - note: no information is stored from the payment form, other than a token reference for verification. All BasketItems are converted to OrderItems, with each OrderItem representing a single-item, i.e. quantity of 1.

Given that this process is only called once payment has been updated, the status of the Order is set to PAID. This is not the default status because an admin could manually create a new order without payment having been received.

d) **Customised Admin Functionality:** Given the importance of clearly understanding order pipeline, the admin area has been heavily customised. OrderItems are displayed as part of the Order (as with BasketItems in Basket).

Focus has been placed on ensuring that admins are able to clearly identify the status of orders upfront, hence the list view includes an editable order status. When viewing the detail of a specific order, each order item also contains a similiar breakdown, clearly detailing status of each individual item.

The aforementioned customisations have been made with workflow management in mind.

e) **Custom Mixins:** I had originally planned to develop this functionality using Class Based Views (CBV) but could not find a way to process two forms on one page. However, whilst pursuing this avenue I created a custom mixin, which would only permit a user to access the checkout view if they had at least one item in their basket, otherwise they would be redirected. Presently, this mixin is not used, however, if I decide to refactor using CBV I will use it to restrict access.

#### Orders

The Orders app is used to display information on user and store orders. At present this is limited to user order history, however, in future it may be extended to include other functionality - see 'Features to be Implemented'.

This app contains on view, Order History, which is only accessible to user's logged in to their acccount. It displays a list of all orders, by date, and the status of, both the overall order and the individual items within the order.

#### Pages

The Pages app is used to website pages which are not related to any specific app. In this instance, the homepage and about us page are delivered via this app. It sets up the urls and delivers the templates to the end user.

#### Products

The Products app provides the majority of the application's functionality. It delivers this through two models, Product and Review.

The Product model enables the site administrator to add/edit/remove products, with custom templates (i.e. outside Django Admin), providing a layer of seperation, with only staff given permission to do so. For example, if a member of staff only needs to add/edit/remove products, they can be given the individual permissions to these functions and access them from the front-end website, they do not need access to the Django Admin area.

From the front-end user perspective, this app provides the views and templates to list the products and enable the user to interact with them. It also enables users to add reviews for products they have purchased.

The functionality of this app is detailed below:

a) **Add/Edit/Remove Products from the Front-end:** Custom views have been written to enable staff to perform CRUD functions from the main website. If the user has the required permission admin functionality will appear throughout the product areas, for example, on a product detail view they will be presented with a dropdown menu to update or delete the product.

Having this functionality built-in to the main website, and not hidden away in the Django Admin area, makes for a more user friendly experience.

b) **Product Views:** Products are displayed either in list form, for multiple views, or in detail form, for a specific product. Within the detail view a user will be able to view product reviews, and add their own, if they have purchased the product previously. Listing views are paginated.

Product ratings are displayed for all products, which are an aggregate of the review scores for each product. The rating stars are produced using a Django custom template tag as detailed below.

c) **Product Search:** To provide users with an optimal experience, reducing the number of steps it takes them to add items to their basket, a search function is incorporated into the Navbar, thus appearing on all pages.

The search functionality performs a case-insensitive search across the product fields, 'title', 'brand', 'category', and, 'description' for matches. Any results are displays in a list view with pagination.

d) **Custom Template Tags:** In order to provide a more visual and user friendly experience for product reviews I wanted to provide star rating. To do so I had to write a custom templatetag which takes in the average product rating and uses this to produce HTML output which assigns the 'checked' class to all those stars up to and including the score. For example, a product with an average rating of 3 will have 3 stars render with 'checked' css class and 2 stars render with 'unchecked'.

e) **Product Reviews:** As noted previously, product ratings are displayed throughout the ecommerce application. These are driven by product reviews. Product reviews can only be left by users who have purchased a product previously. If the user has access to do so, a form will be automatically displayed on the product detail view.

f) **Customised Admin Functionality:** Similarly to the customisation made for the Basket object, the Product Admin has been customised to list all product reviews under the product within the admin website. This makes it easy to manage product reviews.

#### Settings

Normally Django settings are contained within a single file, settings.py, within the project folder. However, in the interest of security and trackability, I have created a settings folder. This contains a number of files which are detailed below:

a) **base.py:** this contains the 'base' settings which are common across all environments that this application has been deployed on. This does not contain any sensitive information. Some of the specific deployment files, listed after this, may override some of these settings if necessary.

b) **local.py:** this contains all settings specific to my local development environment, for example, permissible addresses, database accesses, etc.

c) **test.py:** this contains the settings required to deploy to my test environment, in this case, these are the settings I use to run my application on Travis CI.

d) **production.py:** these are the settings used for deployment in the production environment.

### Features to be implemented

- Automated stock control

- Order processing with custom front-end

- Email when orders are set to completed (i.e. items shipped)

- Order history provides granular breakdown of items in the order

- Edit/Update product reviews

- Add product tags which can be used for filtering

- Product list view filtering, for example, all products between €5.00 - €9.99

## Challenges

## Technologies Used

- [HTML](https://www.w3schools.com/html/default.asp)
  - This is the most fundamental component of a web page, providing the structure and content which can then be then be styled by CSS and interacted with by JavaScript.

- [CSS](https://www.w3schools.com/css/default.asp)
  - This is a styling language which is used to modify how the HTML is render to the user, for example, the fonts used, colours, sizes, etc.
  - To override default Bootstrap styling and provide my own custom styling I have created my own CSS file, base.css, which is applied to every page.

- [JavaScript](https://www.w3schools.com/Js/)
  - This language enables an interactive element to be added to websites, permitting realtime responsive pages.
  - I have used to this to create a payment.js file for interacting with Stripe v3. The JS functionality listens for responses from the Stripe API and provides feedback accordingly. If the payment is successful, a hidden input field is added to the form with a Stripe PaymentIntent ID, for verifying on the server when the form is submitted.

- [Python](https://www.python.org/)
  - This is the server side language the application has been developed using.

- [PostgreSQL](https://www.postgresql.org/)
  - This is an open source database which I have developed the application on.
  - I have created a docker container which runs PostgreSQL and interacts with the Python application.

- [Docker](https://www.docker.com/)
  - This is a technology which packages up applications into containers and runs them in an isolated container within a chosen operating system, which is seperate from the host operating system.
  - The reason I chose to use Docker was it enabled me to create a container with two apps, one for the ecommerce application, and, another for my PostgreSQL database. The apps are then run within a docker image OS, which keeps them seperate from my host machine. It also enables me to control the exact packages added to each app, similiar to virtualenv but with much more minute control.

### Frameworks

- [Bootstrap](https://getbootstrap.com/)
  - This is a front-end framework which is built using HTML and CSS. It makes it easy to create responsive websites using a grid system with screen-width breakpoints.
  - The homepage 'Most Popular' and 'New Products' functionality is partially provided by the Bootstrap Carousel feature.
  - Badges are used to provide the item count above the basket; they are also used to detail the status of each individual item status on the Order History page.

- [JQuery](https://jqueryui.com/)
  - This is a JavaScript framework which enables easy manipulation of the Document Object Model (DOM) using JQuery syntax.
  - This was used to provide the interactive functionality for the homepage carousels. I customised some JavaScript code I found on the internet (see credits) in order to have multiple carousels on one page.

- [Font Awesome](https://fontawesome.com/)
  - This is a font library which I have used to provide some context appropriate icons throughout the application. For example, the Basket icon.

- [Django](https://www.djangoproject.com/)
  - This is a high-level python framework which provides advanced functionality with minimal effort from the developer.
  - The application is developed using Django and extensively uses built-in functionality and custom packages.

- [Django-allauth](https://www.intenct.nl/projects/django-allauth/)
  - This package is an add-on app for Django which implements a third-party authentication system. It provides advanced functionality, such as the integration of external social authentication, e.g. allowing users to authenticate with your website using their Google account, in addition to local authentication.
  - For this application I have used this package for its additional security, as it will only permit a user to attempt to login with incorrect details 5 times before restricting their ability to do so. This is important given it is an ecommerce application. It also enabled me to develop the application using email address as the user login and remove the unneccessary username field in the custom user model.

- [Django-crispy-forms](https://github.com/django-crispy-forms/django-crispy-forms)
  - This package renders Django forms using Bootstrap conventions and classes, effectively making the forms responsive and mobile-first.
  - It also permits customisation of form rendering, from layout, to individual field styles.
  - I have used this package throughout to provide better structured forms with responsive design.

### Third-party services

- [Stripe](https://stripe.com/)

- [Travis CI](https://travis-ci.org/)

- [CodeCov](https://codecov.io/)

## Testing

### Automated

### PEP8

### Manual

## Deployment

### Remote (Heroku)

### Local

## Credits

### Media

Flaticon

Django for Professionals by William S. Vincent.
[Homepage Carousel](https://azmind.com/bootstrap-carousel-multiple-items/)
