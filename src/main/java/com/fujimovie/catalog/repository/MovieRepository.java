package com.fujimovie.catalog.repository;

import com.fujimovie.catalog.model.Movie;
import org.springframework.stereotype.Repository;

import javax.annotation.PostConstruct;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Collectors;

@Repository
public class MovieRepository {
    private final List<Movie> movies = new ArrayList<>();

    @PostConstruct
    public void init() {
        movies.add(new Movie(1L, "El viaje final", "Aventura", 125, 2023, "Laura Mendoza"));
        movies.add(new Movie(2L, "Sombra de plata", "Drama", 110, 2021, "Carlos Rivera"));
        movies.add(new Movie(3L, "Ritmo urbano", "Música", 98, 2024, "Ana Torres"));
        movies.add(new Movie(4L, "Horizonte azul", "Ciencia ficción", 140, 2022, "Miguel Santos"));
        movies.add(new Movie(5L, "Noches de terror", "Terror", 95, 2020, "Sofía Blanco"));
    }

    public List<Movie> findAll() {
        return new ArrayList<>(movies);
    }

    public List<Movie> findByCategory(String category) {
        return movies.stream()
                .filter(movie -> movie.getCategory().equalsIgnoreCase(category))
                .collect(Collectors.toList());
    }

    public List<Movie> findByDurationRange(int minMinutes, int maxMinutes) {
        return movies.stream()
                .filter(movie -> movie.getDurationMinutes() >= minMinutes && movie.getDurationMinutes() <= maxMinutes)
                .collect(Collectors.toList());
    }

    public List<Movie> findByYear(int year) {
        return movies.stream()
                .filter(movie -> movie.getYear() == year)
                .collect(Collectors.toList());
    }

    public List<Movie> findByDirector(String director) {
        return movies.stream()
                .filter(movie -> movie.getDirector().equalsIgnoreCase(director))
                .collect(Collectors.toList());
    }
}
