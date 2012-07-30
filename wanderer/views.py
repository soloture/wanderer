from flask import Flask, request, session, g, redirect, url_for, render_template, flash, abort
from coordinate import move, calculate
from wanderer import app
import random

lat = random.triangular(0,90)
log = random.triangular(0,90)
current = []
destination = []
current.append(lat)
current.append(log)
destination.append(lat)
destination.append(log)


@app.route('/')
def main():
    curcoo = calculate(current,destination)
    print curcoo
    return render_template('index.html',curcoo = curcoo)
    

if __name__ == '__main__':
    app.run(debug=True)
