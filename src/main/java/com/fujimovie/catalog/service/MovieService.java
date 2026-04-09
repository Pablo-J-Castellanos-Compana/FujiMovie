package com.fujimovie.catalog.service;

import com.fujimovie.catalog.model.Movie;
import com.fujimovie.catalog.repository.MovieRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class MovieService {

    private final MovieRepository movieRepository;

    public MovieService(MovieRepository movieRepository) {
        this.movieRepository = movieRepository;
    }

    public List<Movie> getAllMovies() {
        return movieRepository.findAll();
    }

    public List<Movie> getMoviesByCategory(String category) {
        return movieRepository.findByCategory(category);
    }

    public List<Movie> getMoviesByDurationRange(int minMinutes, int maxMinutes) {
        return movieRepository.findByDurationRange(minMinutes, maxMinutes);
    }

    public List<Movie> getMoviesByYear(int year) {
        return movieRepository.findByYear(year);
    }

    public List<Movie> getMoviesByDirector(String director) {
        return movieRepository.findByDirector(director);
    }
}
