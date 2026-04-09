package com.fujimovie.catalog.controller;

import com.fujimovie.catalog.model.Movie;
import com.fujimovie.catalog.service.MovieService;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/api/movies")
public class MovieController {

    private final MovieService movieService;

    public MovieController(MovieService movieService) {
        this.movieService = movieService;
    }

    @GetMapping
    public List<Movie> listMovies(
            @RequestParam(required = false) String category,
            @RequestParam(required = false) Integer minDuration,
            @RequestParam(required = false) Integer maxDuration,
            @RequestParam(required = false) Integer year,
            @RequestParam(required = false) String director
    ) {
        if (category != null) {
            return movieService.getMoviesByCategory(category);
        }
        if (minDuration != null || maxDuration != null) {
            int min = minDuration != null ? minDuration : 0;
            int max = maxDuration != null ? maxDuration : Integer.MAX_VALUE;
            return movieService.getMoviesByDurationRange(min, max);
        }
        if (year != null) {
            return movieService.getMoviesByYear(year);
        }
        if (director != null) {
            return movieService.getMoviesByDirector(director);
        }
        return movieService.getAllMovies();
    }
}
