//hoi sven
#include <iostream>
#include <stdlib.h>

#include <fstream>
#include <iomanip>
#include <limits>

#include <cstdlib>
#include <complex>
#include <math.h>

#define PI 3.14159265

std::ifstream INPUT;
std::ofstream PLOT;
std::fstream R9K;
std::ofstream CHECK;

void Mandelbrot(long double range[4], int iterations, long double xres, long double yres) //range[ left, top, right, bottom ]
{
	for(long double y = range[1]; y >= range[3]; y-=yres)
	{
		for(long double x = range[0]; x <= range[2]; x+=xres)
		{
			long double ronald[2] = {x, y};
			for(int it = 0; it < iterations; it++)
			{
				long double ranranruu = ronald[0]*ronald[0] - ronald[1]*ronald[1] + x;
				ronald[1] = 2*ronald[0]*ronald[1] + y;
				ronald[0] = ranranruu;
				if(ronald[0]*ronald[0]+ronald[1]*ronald[1] > 4)
				{
					PLOT << x << ' ' << y << ' ' << it << std::endl;
					break;
				}
			}
		}
	}
}

void JuliaSets(long double range[4], int iterations, float value[2], long double xres, long double yres)
{
	for(long double y = range[1]; y >= range[3]; y-=yres)
	{
		for(long double x = range[0]; x <= range[2]; x+=xres)
		{
			long double VOORWAARTS[2] = {x, y};
			for(int it = 0; it < iterations; it++)
			{
				long double EENMETDESTORM = VOORWAARTS[0]*VOORWAARTS[0] - VOORWAARTS[1]*VOORWAARTS[1] + value[0];
				VOORWAARTS[1] = 2*VOORWAARTS[0]*VOORWAARTS[1] + value[1];
				VOORWAARTS[0] = EENMETDESTORM;
				if(VOORWAARTS[0]*VOORWAARTS[0] + VOORWAARTS[1]*VOORWAARTS[1] > 4 && it > 0)
				{
					PLOT << x << ' ' << y << ' ' << it << std::endl;
					break;
				}
			}
		}
	}
}

void IFS(long double range[4], int iterations, float parameters[][6], int n)
{
	long double FOO_FIGHTERS[2] = {0, 0};
	for(int it = 0; it < iterations; it++)
	{
		long double old[2] = {FOO_FIGHTERS[0], FOO_FIGHTERS[1]};
		int index = (double) rand()*n / (RAND_MAX);
		FOO_FIGHTERS[0] = parameters[index][0]*old[0] + parameters[index][1]*old[1] + parameters[index][4];
		FOO_FIGHTERS[1] = parameters[index][2]*old[0] + parameters[index][3]*old[1] + parameters[index][5];
		PLOT << FOO_FIGHTERS[0] << ' ' << FOO_FIGHTERS[1] << ' ' << 1 << std::endl;
	}
}

void Sierpinski(long double range[4], int iterations, long double distance, long double polygon[][2], int n)
{
	long double NEHALENNIA[2] = {0, 0};
	for(int it = 0; it < iterations; it++)
	{
		int index = (double) rand()*n / (RAND_MAX);
		NEHALENNIA[0] = (NEHALENNIA[0] + polygon[index][0])*distance;
		NEHALENNIA[1] = (NEHALENNIA[1] + polygon[index][1])*distance;
		PLOT << NEHALENNIA[0] << ' ' << NEHALENNIA[1] << ' ' << 1 << std::endl;
	}
}

int main()
{
	INPUT.open("TEXT/input.txt");
	PLOT.open("TEXT/plot.txt", std::ofstream::out | std::ofstream::trunc);
	R9K.open("TEXT/R9K.txt");
	CHECK.open("TEXT/check.txt", std::ofstream::out | std::ofstream::trunc);
	
	int precision = std::numeric_limits<double>::max_digits10;
	PLOT << std::setprecision(precision);
	
	long double range[4];
	int screen[2], iterations, fractal;
	R9K >> fractal >> range[0] >> range[1] >> range[2] >> range[3] >> screen[0] >> screen[1];;
	switch(fractal)
	{
		case 0:
		{
				INPUT >> iterations;
				//std::cout << (range[2] - range[0])/screen[0] << (range[1] - range[3])/screen[1];
				Mandelbrot(range, iterations, ((range[2] - range[0])/screen[0])*0.9, ((range[1] - range[3])/screen[1])*0.9);
				break;
		}
		case 1:
		{
				int n;
				float distance;
				INPUT >> iterations >> n >> distance;
				long double parameters[n][2];
				for(int i=0; i < n; i++)
				{
					parameters[i][0] = cos(2*PI*i/n);
					parameters[i][1] = sin(2*PI*i/n);
				}
				Sierpinski(range, iterations, distance, parameters, n);
				break;
		}
		case 2:
		{
				float parameters[2];
				INPUT >> iterations >> parameters[0] >> parameters[1];
				JuliaSets(range, iterations, parameters, ((range[2] - range[0])/screen[0])*0.9, ((range[1] - range[3])/screen[1])*0.9);
				break;
		}
		case 3:
		{
				int r;
				INPUT >> iterations >> r;
				switch(r-1)
				{
					case 0:
					{
						float HEIDEVOLK[][6] = {{0, -0.5, 0.5, 0, 0.5, 0},{0, 0.5, -0.5, 0, 0.5, 0.5},{0.5, 0, 0, 0.5, 0.25, 0.5}};
						IFS(range, iterations, HEIDEVOLK, 3);
						break;
					}
					case 1:
					{
						float HEIDEVOLK[][6] = {{0, 0.577, -0.577, 0, 0.0951, 0.5893},{0, 0.577, -0.577, 0, 0.4413, 0.7893},{0, 0.577, -0.577, 0, 0.0952, 0.9893}};
						IFS(range, iterations, HEIDEVOLK, 3);
						break;
					}
					case 2:
					{
						float HEIDEVOLK[][6] = {{0.382, 0, 0, 0.382, 0.3072, 0.619},{0.382, 0, 0, 0.382, 0.6033, 0.4044},{0.382, 0, 0, 0.382, 0.0139, 0.4044}, {0.382, 0, 0, 0.382, 0.1253, 0.0595}, {0.382, 0, 0, 0.382, 0.492, 0.0595}};
						IFS(range, iterations, HEIDEVOLK, 5);
						break;
					}
					case 3:
					{
						float HEIDEVOLK[][6] = {{0.195, -0.488, 0.344, 0.443, 0.4431, 0.2452},{0.462, 0.414, -0.252, 0.361, 0.2511, 0.5692},{-0.058, -0.07, 0.453, -0.111, 0.5976, 0.0969},{-0.035, 0.07 -0.469, -0.022, 0.4884, 0.5069},{-0.637, 0, 0, 0.501, 0.8662, 0.2513}};
						IFS(range, iterations, HEIDEVOLK, 5);
						break;
					}
					case 4:
					{
						float HEIDEVOLK[][6] = {{0.849, 0.037, -0.037, 0.849, 0.075, 0.183},{0.197, -0.226, 0.226, 0.197, 0.4, 0.049},{-0.15, 0.283, 0.26, 0.237, 0.575, -0.084},{0, 0, 0, 0.16, 0.5, 0}};
						IFS(range, iterations, HEIDEVOLK, 4);
						break;
					}
				}
				break;
		}
		default:
				break;
	}
	CHECK << '1';
	CHECK.close();
	exit(EXIT_FAILURE);
}