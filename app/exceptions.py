from fastapi.responses import HTMLResponse
from fastapi import status





async def not_found(request, exc):

    x = """<html lang="en">
           <head>
               <meta charset="UTF-8">
               <meta name="viewport" content="width=device-width, initial-scale=1.0">
               <title>404 Not Found</title>
               <style>
                   body {
                       background-color: black;
                       margin: 0;
                       padding: 0;
                       display: flex;
                       flex-direction: column;
                       align-items: center;
                       justify-content: center;
                       height: 100vh;
                   }
           
                   h1 {
                       font-size: 72px;
                       color: white;
                       text-align: center;
                   }
           
                   p {
                       font-size: 24px;
                       color: white;
                       text-align: center;
                   }
           
                   a {
                       text-decoration: none;
                       color: #3498db;
                   }
           
                   a:hover {
                       text-decoration: underline;
                   }
               </style>
           </head>
           <body>
               <h1>404 Not Found</h1>
               <p>Sorry, the page you're looking for could not be found.</p>
               <p><a href="/">Go back to the homepage</a></p>
           </body>
           </html>
           
           """

    content = {"message" : "page not found"}
    return HTMLResponse(content=x, status_code=status.HTTP_404_NOT_FOUND)

