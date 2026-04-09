package com.fujimovie.catalog.model;

public class Movie {
    private Long id;
    private String title;
    private String category;
    private int durationMinutes;
    private int year;
    private String director;

    public Movie() {
    }

    public Movie(Long id, String title, String category, int durationMinutes, int year, String director) {
        this.id = id;
        this.title = title;
        this.category = category;
        this.durationMinutes = durationMinutes;
        this.year = year;
        this.director = director;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public int getDurationMinutes() {
        return durationMinutes;
    }

    public void setDurationMinutes(int durationMinutes) {
        this.durationMinutes = durationMinutes;
    }

    public int getYear() {
        return year;
    }

    public void setYear(int year) {
        this.year = year;
    }

    public String getDirector() {
        return director;
    }

    public void setDirector(String director) {
        this.director = director;
    }
}
