
# THE Pet Store

[![Build Status](https://travis-ci.org/jyoung90ie/django-ecommerce.svg?branch=master)](https://travis-ci.org/jyoung90ie/django-ecommerce)
[![codecov](https://codecov.io/gh/jyoung90ie/django-ecommerce/branch/master/graph/badge.svg)](https://codecov.io/gh/jyoung90ie/django-ecommerce)

This is a project for the final milestone project at [Code Institute](https://codeinstitute.net/) to demonstrate my learning and understanding throughout the course. I chose to develop an ecommerce shopping website as it is a complex and flexible application which challenged my understanding of the technologies involved. Given the sensitivity involved in handling customer details I had to approach development from a security conscious perspective.

Overall I believe I produced an application that is very adaptable and can be repurposed for many ecommerce applications, including subscriptions and transactional services. There are a number of features which I would have liked to include for submission of my milestone project, however, due to time constraints these were not feasible at this point-in-time.

## Deployed Application

You can access the application [here](https://jy-djangoapp.herokuapp.com). If you wish to test account functionality, demo accounts have been provided below. Please note email functionality has not been configured yet, any messages related to emails can be ignored.

## Demonstration Data & Accounts

To enable you to test the website functionality, a number of demo accounts, products, and, transactions have been created. You can access this data using the accounts below. Note delete permissions have not been included to preserve test data.

| Email | Password | Desription |
| ----- | -------- | ---------- |
| customer@test.com | test_1234 | Customer account with an multiple orders. |
| staff@test.com | test_1234 | Staff account with create and update permissions to the Product model, but no permission to admin area. You will see dropdown menus appear on product listing and product detail page |
| admin@test.com | test_1234 | Admin account with create and update permissions to all custom models, these are accessible in the access admin area. |

## UX

Given this application is for an ecommerce website, the design is very product and customer centric. It has been designed to enable a customer to add items to their basket, and checkout and pay as seamlessly as possible. All pertinent product information is highlighted upfront, for example, price and rating, to keep customers informed. The menu becomes fixed at the top so the user always knows where they are and can quickly navigate to where they want to go.

### Wireframes

Prior to development of the application, I developed a number of wireframes which demonstrate my vision for how the website should look on multiple devices. You can view these wireframes [here](wireframes/).

### User Stories

#### Customer

As a customer I want to be able to...

- Add products to my basket as I browse the website, so that I can continue to browse the website and add more items if I wish.
- Specify the quantity I would like of each item in my basket, so that I can order multiple items.
- Search for products, so I can quickly determine if a product is stocked, or find a product I ordered previously.
- View product ratings and reviews, so that I can see feedback from other users to determine if a product is a good fit for me.
- Add reviews for products I have purchased, so that I feel that I can contribute to product development and community.
- Pay for my basket of products using my bank card, so that I do not need to do any unneccessary steps, like bank transfers.
- View my order history, so that I can see a breakdown of items I've previously purchased.
- View the status of my order(s), so that I have confidence that my order is being processed.
- update my personal details, including email and password, so that I can self-service as needed.
- create and pay for an order without any unneccessary steps, so that I can quickly place orders on-the-go.
- Trust that the company I am transacting with will handle my data securely, so that I do not need to worry about fraud.
- View detailed product information, so that I can drill into the specific product information I need, for example, product dimensions.

#### Store Owner

As the store owner, I want the ability to ...

- Add new products and have them automatically display on the website, so that customers can purchase them.
- Edit product details, for example, price and stock.
- Remove products from display, so that if I have supply issues I can prevent customers from viewing it.
- View the status of all customer orders, so that I can efficiently manage the orders.
- View the most popular products, so that I can ensure I maintain higher stock levels for these items.
- Link customer orders to the Stripe PaymentIntent dashboard, so that I can verify custom payment details, if I need to.
- Manage customer reviews, so that I any inappropriate content can be removed if necessary.
- Update individual items with a customer's order, so that I can keep customers informed and to manage my workflow.
- Update customer orders, so that customers are notified in realtime.
- View all active baskets, so that I can issue targeted discounts to increase basket conversion.


## Features

### Existing Features

This package enables you to build and deploy a functional ecommerce website, with payment processing through the secure third-party service, [Stripe](https://stripe.com/).

The package has been broken into individual apps, the features of which are detailed under each of the headings below.

#### Custom User Model

To capture additional user information, such as address, I opted to override the default Django user model and create a custom one. This enabled me to store all the necessary user data in one object. It will also make any future user model changes easier to make.

Given the additional data input requirements, I had to specify custom forms in order to capture all the required information. This included overriding Django default forms, for example, the admin forms for adding/modifying user details.

#### Accounts

This is where all customer information is retained via the custom user model. I also made the decision to use Django-allauth which added the ability to override the username field, using the email address as the login. It also brought with it the ability to verify email addresses and reset passwords.

Within this app I have overriden a number of the default forms provided by allauth to integrate with the customer user model. To produce responsive forms I have used the django-crispy-forms helper function which allows me to create custom form layouts with individual element styling. I have also modified the rendering of the django admin site for the user object, to provide a better structure.

Outlined below are the views that are produced by this app:

a) **Signup:** a custom form used to create a new user account with the custom user model. The username field is removed, with the email address used in it's placed. Given this is an ecommerce application, it made more sense to proceed with email only, as a username would not serve any other function than to login.

b) **Login:** Enables users to login using their email address and password. If any products exist in a user's basket before they login, these will be merged into any existing basket when the user logs in.

c) **Logout:** Enables users to logout of their account. The user will be asked to confirm they wish to logout of their account, this prevents accidental logout. When a user logs out any items added to their basket will no longer be visible, however, the basket will be stored in the account and visible upon login.

d) **Profile - Personal Details:** The user can update their billing address from here. I made the decision to *only* allow billing address to be changed here for security, so that a user can only use payment cards for one billing address. The billing address is passed through to Stripe upon payment processing. When updating details the user will be provided with feedback flash messages to give a more interaction experience and confirm to the user if an update took place or not.

e) **Profile - Change email:** A user can have multiple emails if they wish, this functionality is leveraged from django-allauth. The user can log in with all email addresses under their account. I decided to include this functionality to enable users to have one householder account if they wish.

f) **Profile - Change password:** For security, a user must provide their current password alongside a new password before it will be accepted and updated.

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

From the front-end user perspective, this app provides the views and templates to list the products and enable the user to interact with them. It also enables users to add reviews for products.

The functionality of this app is detailed below:

a) **Add/Edit/Remove Products from the Front-end:** Custom views have been written to enable staff to perform CRUD functions from the main website. If the user has the required permission admin functionality will appear throughout the product areas, for example, on a product detail view they will be presented with a dropdown menu to update or delete the product.

Having this functionality built-in to the main website, and not hidden away in the Django Admin area, makes for a more user friendly experience.

b) **Product Views:** Products are displayed either in list form, for multiple views, or in detail form, for a specific product. Within the detail view a user will be able to view product reviews, and add their own, in future this will be confined to users that have purchased the product. Listing views are paginated.

Product ratings are displayed for all products, which are an aggregate of the review scores for each product. The rating stars are produced using a Django custom template tag as detailed below.

c) **Product Search:** To provide users with an optimal experience, reducing the number of steps it takes them to add items to their basket, a search function is incorporated into the Navbar, thus appearing on all pages.

The search functionality performs a case-insensitive search across the product fields, 'title', 'brand', 'category', and, 'description' for matches. Any results are displays in a list view with pagination.

d) **Custom Template Tags:** In order to provide a more visual and user friendly experience for product reviews I wanted to provide star rating. To do so I had to write a custom templatetag which takes in the average product rating and uses this to produce HTML output which assigns the 'checked' class to all those stars up to and including the score. For example, a product with an average rating of 3 will have 3 stars render with 'checked' css class and 2 stars render with 'unchecked'.

e) **Product Reviews:** As noted previously, product ratings are displayed throughout the ecommerce application. These are driven by product reviews. If the user has access to do so, a form will be automatically displayed on the product detail view.

f) **Customised Admin Functionality:** Similarly to the customisation made for the Basket object, the Product Admin has been customised to list all product reviews under the product within the admin website. This makes it easy to manage product reviews.

#### Settings

Normally Django settings are contained within a single file, settings.py, within the project folder. However, in the interest of security and trackability, I have created a settings folder. This contains a number of files which are detailed below:

a) **base.py:** this contains the 'base' settings which are common across all environments that this application has been deployed on. This does not contain any sensitive information. Some of the specific deployment files, listed after this, may override some of these settings if necessary.

b) **local.py:** this contains all settings specific to my local development environment, for example, permissible addresses, database accesses, etc.

c) **test.py:** this contains the settings required to deploy to my test environment, in this case, these are the settings I use to run my application on Travis CI.

d) **production.py:** these are the settings used for deployment in the production environment.

### Features to be implemented

- Email configuration to enable the application to send emails

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
  - To use Bootstrap tabs with the template I had to write custom JS code to override the default Bootstrap.js function and replace it with code that worked for me.
  - The navigation menu becomes fixed once the user scrolls past the header and brand container, this is achieved using custom JS code and Bootstrap classes.

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
  - This is used to securely process customer payment details. No payment data is handled or stored by the application, it is all handled by Stripe. This makes for easy and secure integration and verification of payments.

- [Travis CI](https://travis-ci.org/)
  - Everytime a new commit is pushed to Github Travis CI performs the testing I have specified in the travis.yml configuration file.
  - This automtically alerts me to any new commits which have resulted in a broken build, which helps me to quickly identify and fix problems with deployment of new code.
  - I have also setup Travis CI to run Flake8, which is a wrapper for a number of other tools that check ensure compliance with PEP8 and good coding practices.
  - Travis CI runs all testing through the Python coverage tool which outputs documentation detailing how much of the development code has been unit tested. I have set this up to provide the results to CodeCov (see below) for coverage transparency.

- [CodeCov](https://codecov.io/)
  - This is a reporting tool that is used to transparently show what code has and has not been tested within an application.
  - In my case I have included a coverage badge at the top of this readme, showing how much of my development code is currently tested.
  - I have implemented a personal goal to only commit code that will result in this coverage percentage either remaining the same or increasing. I believe this is a good coding practice to enforice.
  - This tool has helped me easily identify areas that I need to improve testing of.

## Testing

### Automated

Within the overall ecommerce application, each app has a testing module which contains extensive unit testing. This is all visible within Github and will demonstrate the extent of the testing. However, if you would like to understand the coverage of the unit testing this can be found on at the [CodeCov repo](hhttps://codecov.io/gh/jyoung90ie/django-ecommerce/)

### Manual

In addition to the automated testing, I conducted some manual testing across a number of browsers and devices. This was to ensure, the pages rendered as expected, and that screen space was optimally utilised.

| # | Test | Test Criteria | Result |
|---|------|--------|------|
| 1 | Website is displayed correctly on multiple browsers | Tested on Chrome, Safari, and Edge | Passed |
| 2 | Website is responsive and displayed correctly on multiple devices | Tested on Macbook Pro, Windows Laptop, Samsung S9+, and iPhone | Passed |
| 3 | Forms do not permit entry of invalid data; invalid entries receive an error message | Attempting to update basket quantity to more than the maximum permitted amount (i.e. > 5) | Passed |
| 4 | All links work | Check that all links are work | Passed |
| 5 | Images, icons, and buttons render correctly | Visual inspection of every page | Passed |

### Known bugs

- When running the automated testing suite, product objects are created which require images. The images created are not deleted after the tests have run, these need to be manually removed each time.

## Deployment

### Stripe (Payments API) setup

Prior to deploying the application to Heroku it is recommended that you create a Stripe account to use the payment processing functionality - note: the application is set for test payments only. Follow the steps below to create an account and to retrieve the necessary keys you will need later.

1. Create an account at [Stripe](https://dashboard.stripe.com/register)

2. Goto the [account dashboard](https://dashboard.stripe.com/test/dashboard).

3. Click the _Developers_ link then [API keys](https://dashboard.stripe.com/test/apikeys)

4. You will see two keys; `Publishable key` and `Secret key`. Keep these private, you will need them later when setting environment variables in Heroku.

| Stripe Key | Maps to Environment Key |
| ---------- | ----------------------- |
| Publishable key | STRIPE_TEST_PUBLISHABLE |
| Secret key | STRIPE_TEST_SECRET |

### Remote (Heroku)

1. Create an account at [Heroku](https://www.heroku.com/).

2. Download CLI [here](https://devcenter.heroku.com/articles/getting-started-with-python#set-up).

3. Open up CMD (Windows) or Terminal (MacOS) and type the following and follow the instructions that appear.

```terminal
heroku login
```

4. Create a new Heroku app using the following code in your terminal:

```terminal
heroku create app-name-here
```

5. With the Heroku app name you just created, modified the `production.py` file in the settings folder and update the following:

```python
ALLOWED_HOSTS = ['your-app-name.herokuapp.com', '127.0.0.1', 'localhost']
```

6. Open the [Heroku apps](https://dashboard.heroku.com/apps) webpage and click the app you created in Step 4.

7. Navigate to the Settings tab on the top horizontal bar, we will be adding the required _environment variables_ here.

8. Click the _'Reveal Config Vars'_ button and add the below variables:

| KEY  | VALUE |
| ---- | ----- |
| `ENV_SETTINGS` | `settings.production` |
| `SECRET_KEY` | input your own value here |
| `STRIPE_TEST_PUBLISHABLE` | input your own value here |
| `STRIPE_TEST_SECRET` | input your own value here |

9. Given the application has been developed within a Docker container, it will be deployed to Heroku using Docker. To enable this, Heroku requires a *[heroku.yml]* file is created. The [Heroku documentation](https://devcenter.heroku.com/articles/build-docker-images-heroku-yml) provides more detail on this.

10. The Heroku stack will need to be set to use container - this is specific to deployment with Docker. You can find out more [here](https://devcenter.heroku.com/articles/stack). To do this type the following command into your terminal:

```terminal
heroku stack:set container -a app-name-here
```

11. You can verify the above was completed by going to your app's overview screen, on the Heroku website and clicking the latest activity, you should see something similiar to:

```text
email@address.com: Upgrade stack to container
```

12. A database is required to run the application, we will use Heroku's free option to do so. This step can be completed using the terminal, with the following code:

```terminal
heroku addons:create heroku-postgresql:hobby-dev -a app-name-here
```

13. To push the code to the Heroku app, a git remote link needs to be added and the code then needs to be pushed. To do this, within your terminal write the following code:

```terminal
heroku git:remote -a app-name-here
git push heroku master
```

14. Given this will be a fresh build, Django will need to create the required databases in our database. Run the following code in your terminal:

```terminal
heroku run python manage.py migrate --settings=settings.production
```

_**NOTE:** `--settings=settings.production` is required because Django by default looks for the file, `settings.py`. This does not exist within this application, instead a settings folder has been setup with different settings dependent on the environment the application is being run on._

15. Next, a superuser account needs to be created to manage the application. Type the following into your terminal:

```terminal
heroku run python manage.py createsuperuser --settings=settings.production
```

16. It is possible to link your Github repository to Heroku so that each time new code is committed to Github, it is also deployed to Heroku and thus your Heroku app is always sync to Github. To do this, nagivate to the following link and input your Github details. You will be prompted to search for the repo name. Once you have selected the repo make sure to click **Enable automatic deploys**.

```url
https://dashboard.heroku.com/apps/app-name-here/deploy/
```

17. To enable product images to be uploaded you will need to install django-storages and use Amazon S3 to store media files. Follow [this excellent guide](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/) to set this up. Follow all the steps for creating an S3 bucket, assigning access, and retrieving the keys to access it. Once you have the access keys you can proceed to the step below.

18. You will need to create some additional environment variables in Heroku - these are outlined below and are self-explantory. (See Steps 6-8 above for a refresher on creating Heroku environment variables)

| KEY  | VALUE |
| ---- | ----- |
| `USE_S3` | `TRUE` |
| `AWS_ACCESS_KEY_ID` | access key you created in Step 17 |
| `AWS_SECRET_ACCESS_KEY` | access key you created in Step 17 |
| `AWS_STORAGE_BUCKET_NAME` | the name of the bucket you created in Step 17 |

19. Run the below command in the Heroku CLI:

```terminal
heroku run python manage.py collectstatic --noinput --settings=settings.production
```

19. Your Heroku deployment is now operational. You can access it via the Heroku dashboard.

### Local machine deployment

If you wish to deploy this application to your local system, you can do so by following the steps below:

1. You will need to download and install [Docker Desktop](https://www.docker.com/get-started)

2. Download and install Git to your computer - see [here](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git).

3. Once you have installed Git, you will need to create a folder on your computer and then run the _git clone_ command. A demonstration of this code can be seen below:

```terminal
mkdir ecommerceApp
cd ecommerceApp
git clone https://github.com/jyoung90ie/django-ecommerce
```

**_The following steps should all be performed while in the root folder of your travelPal git clone from step 2_**

4. Download and install [Python](https://www.python.org/downloads/)

5. Then install `docker-compose` using the following terminal command:

```
pip install docker-compose
```

5. Now the docker container needs to be built. Navigate to the root folder in the terminal (_ecommerceApp_) and input the code below.

```terminal
docker-compose up -d --build
```

*Depending on your ISP and/or computer speed this may take some time as it has to download large image files. Let it complete before proceeding.*

6. Create a .env file and input the variables outlined below:

| KEY  | VALUE |
| ---- | ----- |
| `DB_NAME` | `postgres` |
| `DB_USER` | `postgres` |
| `DB_PASS` | `postgres` |
| `DB_HOST` | `db` |
| `DB_HOST` | `5432` |
| `SECRET_KEY` | input-a-value-here |
| `STRIPE_TEST_PUBLISHABLE` | input value from the Stripe deployment section |
| `STRIPE_TEST_SECRET` | input value from the Stripe deployment section |

7. Now that the docker container is running, run the following commands to create the databases required and create a super user.

```terminal
docker-compose exec web python manage.py migrate --settings=settings.production
docker-compose exec web python manage.py createsuperuser --settings=settings.production
```

8. The application will now be viewable at the following address:

```url
http://127.0.0.1:8000
```



## Credits

### Content

- [About Page](http://www.petbusiness.com/A-Short-History-of-the-Pet-Industry/)

### Media

- [Product Images](https://images.google.com/)
  - All product images were sourced from Google.

### Acknowledgements

- [Theme Wagon](https://demo.themewagon.com/preview/free-bootstrap-ecommerce-template)
  - I leveraged the product layout and some styling from this template and embedded it with my own styling and tweaks.

- [UI Cookies - Bootstrap Footer](https://uicookies.com/bootstrap-footer/)
  - I leveraged the templates on this page to create the footer.

- [Homepage Carousel](https://azmind.com/bootstrap-carousel-multiple-items/)

- [Django for Professionals by William S. Vincent](https://wsvincent.com/books/djangoforprofessionals)
  - This book helped me embed some best practices throughout development, including the value of using Docker for development and deployment. I highly recommend it.
