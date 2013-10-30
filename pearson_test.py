def test():
    movie = session.query(Movie).filter_by(title="Toy Story").one()
    user1 = session.query(User).get(1)
    user2 = session.query(User).get(2)

    other_ratings = session.query(Rating).filter_by(movie_id=m.id).all()
    other_users = []
    for r in other_ratings:
        other_users.append(r.user)


    rating_pairs = []
    overlap = {}

    for rating in user1.ratings:
        overlap[rating.movie_id] = rating.rating

    for rating in user2.ratings:
        if overlap.get(rating.movie_id) != 0:
            rating_pairs.append((overlap.get(rating.movie_id), rating.rating))
